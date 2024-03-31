import { useContext, useEffect } from "react";
import { ChatContext } from "../context/ChatContext.tsx";
import { io } from "socket.io-client";
import { AppContext } from "../context/AppContext.tsx";
import { sendStartSession } from "../lib/websocketFunctions.ts";
import { saveSession } from "../lib/sessionFunctions.ts";
import { WEBSOCKET_SERVER_COMMAND } from "../model/websocketCommands.ts";
import { Message } from "../model/message.ts";

interface ServerMessage {
  session_id: string;
  server_messages: Message[];
}

function adaptServerMessages(serverMessages: ServerMessage): Message[] {
  return serverMessages.server_messages.map((message: any) => ({
    question: message.question,
    answer: message.answer,
    final_report: message.final_report,
    suggestions: message.suggestions.map((suggestion: any) => ({
      id: suggestion.id,
      img_alt: suggestion.img_alt,
      img_src: suggestion.img_src,
      main_text: suggestion.main_text,
      title: suggestion.title,
    })),
  }));
}

export function useWebsocket() {
  const { socket, websocketUrl } = useContext(ChatContext);
  const { setConnected, setMessages, setCurrentMessage, setSending } =
    useContext(AppContext);

  useEffect(() => {
    socket.current = io(websocketUrl);

    const onConnect = () => {
      console.info("connected");
      setConnected(true);
      // Handle session
      sendStartSession(socket.current);
    };

    const onDisconnect = () => {
      console.info("disconnected");
      setConnected(false);
    };

    function onStartSession(value: string) {
      if (!value) return;
      const serverMessages = JSON.parse(value);
      setMessages(adaptServerMessages(serverMessages));
      setCurrentMessage(serverMessages.server_messages.length - 1);
      saveSession({ id: serverMessages.session_id, timestamp: new Date() });
    }

    function onServerMessage(value: string) {
      const serverMessages = JSON.parse(value);
      setMessages(adaptServerMessages(serverMessages));
      setCurrentMessage(serverMessages.server_messages.length - 1);
      setSending(false);
    }

    socket.current.on(WEBSOCKET_SERVER_COMMAND.START_SESSION, onStartSession);
    socket.current.on(WEBSOCKET_SERVER_COMMAND.CONNECT, onConnect);
    socket.current.on(WEBSOCKET_SERVER_COMMAND.DISCONNECT, onDisconnect);
    socket.current.on(WEBSOCKET_SERVER_COMMAND.SERVER_MESSAGE, onServerMessage);

    return () => {
      socket.current?.off(
        WEBSOCKET_SERVER_COMMAND.START_SESSION,
        onStartSession,
      );
      socket.current?.off(WEBSOCKET_SERVER_COMMAND.CONNECT, onConnect);
      socket.current?.off(WEBSOCKET_SERVER_COMMAND.DISCONNECT, onDisconnect);
    };
  }, []);
}
