import { Message } from "../model/message.ts";
import { createContext, useState } from "react";
import { Props } from "./commonModel.ts";

interface AppState {
  expectedNodes: number;
  setExpectedNodes: (expectedNodes: number) => void;
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  startSession: boolean;
  setStartSession: (startSession: boolean) => void;
  connected: boolean;
  setConnected: (connected: boolean) => void;
  currentMessage: number;
  setCurrentMessage: (currentMessage: number) => void;
  selectedSuggestion?: string;
  setSelectedSuggestion: (selectedSuggestion: string) => void;
  sending: boolean;
  setSending: (sending: boolean) => void;
  chatText: string;
  setChatText: (chatText: string) => void;
  readonly isLast: boolean;
}

const DEFAULT_EXPECTED_NODES = 6;

function createAppState(): AppState {
  const messages: Message[] = [];
  const expectedNodes = DEFAULT_EXPECTED_NODES;

  return {
    expectedNodes,
    messages,
    startSession: false,
    connected: false,
    sending: false,
    currentMessage: 0,
    chatText: "",
    setStartSession: (_) => {},
    setConnected: (_) => {},
    setMessages: (_: Message[]) => {},
    setCurrentMessage: (_) => {},
    setSelectedSuggestion: (_) => {},
    setSending: (_) => {},
    setExpectedNodes: (_) => {},
    setChatText: (_) => {},
    isLast: true
  };
}

const initial = createAppState();

export const AppContext = createContext<AppState>(initial);

export const AppContextProvider = ({ children }: Props) => {
  const [connected, setConnected] = useState(false);
  const [startSession, setStartSession] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState(0);
  const [selectedSuggestion, setSelectedSuggestion] = useState<string>();
  const [sending, setSending] = useState(false);
  const [expectedNodes, setExpectedNodes] = useState(DEFAULT_EXPECTED_NODES);
  const [chatText, setChatText] = useState("");

  const isLast = currentMessage === messages.length - 1;

  return (
    <AppContext.Provider
      value={{
        ...initial,
        expectedNodes,
        setExpectedNodes,
        connected,
        setConnected,
        startSession,
        setStartSession,
        messages,
        setMessages,
        currentMessage,
        setCurrentMessage,
        selectedSuggestion,
        setSelectedSuggestion,
        sending,
        setSending,
        chatText,
        setChatText,
        isLast
      }}
    >
      {" "}
      {children}{" "}
    </AppContext.Provider>
  );
};
