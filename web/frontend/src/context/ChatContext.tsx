import { createContext, useRef } from "react";
import { Props } from "./commonModel.ts";
import { Socket } from "socket.io-client";

const DEFAULT_WEBSOCKET_URL = "ws://127.0.0.1:5000";

interface ConfigState {
  websocketUrl: string;
  reportUrl: string;
  socket: React.MutableRefObject<Socket | null>;
}

declare global {
  interface Window {
    dataWellnessConfig: any;
  }
}

export const ChatContext = createContext<ConfigState>({
  websocketUrl: "ws://localhost:8080",
  reportUrl: "http://localhost:8080",
  socket: { current: null },
});

export const ConfigContextProvider = ({ children }: Props) => {
  const { dataWellnessConfig } = window;
  const { websocketUrl, reportUrl } =
    dataWellnessConfig || DEFAULT_WEBSOCKET_URL;
  const socket: React.MutableRefObject<Socket | null> = useRef<Socket | null>(
    null,
  );
  return (
    <ChatContext.Provider value={{ websocketUrl, reportUrl, socket }}>
      {children}
    </ChatContext.Provider>
  );
};
