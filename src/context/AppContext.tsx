import { Message } from "../model/message.ts";
import { createContext, useState } from "react";
import { Props } from "./commonModel.ts";

interface AppState {
  expectedNodes: number;
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  startSession: boolean;
  setStartSession: (startSession: boolean) => void;
  connected: boolean;
  setConnected: (connected: boolean) => void;
  currentMessage: number;
  setCurrentMessage: (currentMessage: number) => void;
}

function createAppState(): AppState {
  const messages: Message[] = [];
  const expectedNodes = 6;

  return {
    expectedNodes,
    messages,
    startSession: false,
    connected: false,
    currentMessage: 0,
    setStartSession: (_) => {},
    setConnected: (_) => {},
    setMessages: (_: Message[]) => {},
    setCurrentMessage: (_) => {},
  };
}

const initial = createAppState();

export const AppContext = createContext<AppState>(initial);

export const AppContextProvider = ({ children }: Props) => {
  const [connected, setConnected] = useState(false);
  const [startSession, setStartSession] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState(0);
  return (
    <AppContext.Provider
      value={{
        ...initial,
        connected,
        setConnected,
        startSession,
        setStartSession,
        messages,
        setMessages,
        currentMessage,
        setCurrentMessage,
      }}
    >
      {" "}
      {children}{" "}
    </AppContext.Provider>
  );
};
