import asyncio
import ipaddress
import time
from collections import defaultdict, deque

from aiohttp import web

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.jwt_token_service import decode_token

WINDOW, MAX_REQ = 1.0, 8  # 8 req/sec per IP
CLEANUP_INTERVAL = 300  # Clean up every 5 minutes


@web.middleware
async def rate_limit(request, handler):
    # Only apply rate limiting to socket.io requests
    if not request.path.startswith("/socket.io/"):
        return await handler(request)

    ip = extract_client_ip(request)
    now = time.monotonic()
    q = hits[ip]

    # Clean old timestamps
    while q and now - q[0] > WINDOW:
        q.popleft()

    # Check rate limit
    if len(q) >= MAX_REQ:
        return web.Response(status=429, text="Too Many Requests")

    # Add current request timestamp
    q.append(now)
    return await handler(request)


@web.middleware
async def protected_middleware(request, handler):
    if request.method == "OPTIONS":
        return await handler(request)
        
    if request.path.startswith("/protected/"):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise web.HTTPForbidden(text="Missing or invalid Bearer token")
        token = auth_header.removeprefix("Bearer ").strip()
        if not token:
            raise web.HTTPForbidden(text="Missing Bearer token")
        else:
            decoded = await decode_token(token)
            if decoded is None:
                raise web.HTTPForbidden(text="Failed to decode token")
            return await handler(request)
    else:
        return await handler(request)


async def extract_client_ip(request: web.Request) -> str:
    """Extract and validate client IP address from request headers."""
    # Check X-Forwarded-For header (for reverse proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        client_ip = forwarded_for.split(",")[0].strip()
        try:
            # Validate IP address
            ipaddress.ip_address(client_ip)
            return client_ip
        except ValueError:
            pass

    # Fall back to direct connection IP
    if request.remote:
        try:
            ipaddress.ip_address(request.remote)
            return request.remote
        except ValueError:
            pass

    # If all else fails, return a default identifier
    return "unknown"


hits = defaultdict(deque)


async def cleanup_inactive_ips():
    """Periodically clean up inactive IP addresses to prevent memory leaks."""
    while True:
        try:
            await asyncio.sleep(CLEANUP_INTERVAL)
            now = time.monotonic()
            inactive_ips = []

            for ip, timestamps in hits.items():
                # Remove old timestamps
                while timestamps and now - timestamps[0] > WINDOW:
                    timestamps.popleft()

                # If no recent activity, mark for removal
                if not timestamps:
                    inactive_ips.append(ip)

            # Remove inactive IPs
            for ip in inactive_ips:
                del hits[ip]

            if inactive_ips:
                logger.info(f"Cleaned up {len(inactive_ips)} inactive IP addresses")

        except Exception as e:
            logger.error(f"Error during IP cleanup: {e}")
