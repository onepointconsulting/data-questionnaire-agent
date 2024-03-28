import { Session } from "../model/session.ts";

export const SESSION_KEY = "session";

export function saveSession(session: Session) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function getSession(): Session | null {
  const session = localStorage.getItem(SESSION_KEY);
  if (session) {
    try {
      const sessionObj = JSON.parse(session);
      if (typeof sessionObj.timestamp === "string") {
        return {
          id: sessionObj.id,
          timestamp: new Date(sessionObj.timestamp),
        };
      }
    } catch (e) {
      console.error("Error getting session from local storage", e);
    }
  }
  return null;
}
