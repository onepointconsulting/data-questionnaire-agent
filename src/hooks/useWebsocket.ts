import { useContext, useEffect } from "react";
import { ChatContext } from "../context/ChatContext.tsx";
import { io } from "socket.io-client";
import { AppContext } from "../context/AppContext.tsx";
import { sendStartSession } from "../lib/websocketFunctions.ts";
import { saveSession } from "../lib/sessionFunctions.ts";
import { WEBSOCKET_SERVER_COMMAND } from "../model/websocketCommands.ts";

export function useWebsocket() {
  const { socket, websocketUrl } = useContext(ChatContext);
  const { setConnected, setMessages } = useContext(AppContext);

  // useEffect(() => {
  //   if (!!startSession?.value) {
  //     // Start the session after the configuration is finished.
  //     sendStartSession(socket.current);
  //   }
  // }, [startSession?.value]);

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
      console.log(serverMessages);
      setMessages(
        serverMessages.server_messages.map((message: any) => ({
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
        })),
      );
      saveSession({ id: serverMessages.session_id, timestamp: new Date() });
    }

    socket.current.on(WEBSOCKET_SERVER_COMMAND.START_SESSION, onStartSession);
    socket.current.on(WEBSOCKET_SERVER_COMMAND.CONNECT, onConnect);
    socket.current.on(WEBSOCKET_SERVER_COMMAND.DISCONNECT, onDisconnect);

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
