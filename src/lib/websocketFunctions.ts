import { Socket } from "socket.io-client";
import { WEBSOCKET_COMMAND } from "../model/websocketCommands.ts";
import { getSession } from "./sessionFunctions.ts";

export function sendStartSession(socket: Socket<any, any> | null, expectedInteviewSteps: number | null) {
  const session = getSession();
  safeEmit(socket, WEBSOCKET_COMMAND.START_SESSION, session ? session.id : "", expectedInteviewSteps);
}

export function sendClientMessage(
  socket: Socket<any, any> | null,
  answer: string,
) {
  const session = getSession();
  safeEmit(
    socket,
    WEBSOCKET_COMMAND.CLIENT_MESSAGE,
    session ? session.id : "",
    answer,
  );
}

function safeEmit(
  socket: Socket<any, any> | null,
  event: string,
  ...args: any[]
) {
  if (!!socket) {
    socket.emit(event, ...args);
    console.info(`Sent ${event} message`);
  } else {
    console.warn(`Socket is null, cannot send ${event} message.`);
  }
}
