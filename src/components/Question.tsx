import { AiFillQuestionCircle } from "react-icons/ai";
import { Message } from "../model/message.ts";
import { useEffect, useState } from "react";

const STEP_MILLI_SECONDS = 25;

function incrementalText(text: string, setMessageText: (text: string) => void) {
  let i = 0;
  const interval = setInterval(() => {
    setMessageText(text.slice(0, i));
    i++;
    if (i > text.length) {
      clearInterval(interval);
    }
  }, STEP_MILLI_SECONDS);
}

export default function Question({
  message,
  currentMessage,
  messagesLength,
}: {
  message: Message;
  currentMessage: number;
  messagesLength: number;
}) {
  const [messageText, setMessageText] = useState<string>("");

  useEffect(() => {
    if (currentMessage === 0 && messagesLength < 2) {
      incrementalText(message.question, setMessageText);
    } else {
      setMessageText(message.question);
    }
  }, [message, currentMessage]);

  return (
    <div className="question container">
      <AiFillQuestionCircle />
      <div className="ml-2">{messageText}</div>
    </div>
  );
}
