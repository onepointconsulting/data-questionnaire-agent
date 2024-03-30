import { useContext, useEffect, useRef, useState } from "react";
import { AppContext } from "../context/AppContext.tsx";
import {sendClientMessage} from "../lib/websocketFunctions.ts";
import {ChatContext} from "../context/ChatContext.tsx";

function adjustHeight(style: CSSStyleDeclaration, el: HTMLTextAreaElement) {
  style.height = `auto`;
  style.height = `${el.scrollHeight}px`;
}

/**
 * Chat input field to be used in this application.
 * @constructor
 */
export default function ChatInput() {
  const { selectedSuggestion, setSending, sending, connected } = useContext(AppContext);
  const { socket } = useContext(ChatContext);
  const [text, setText] = useState("");
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (selectedSuggestion && textAreaRef.current) {
      setText(selectedSuggestion);
      const style = textAreaRef.current.style;
      const el = textAreaRef.current;
      adjustHeight(style, el);
    }
  }, [selectedSuggestion]);

  useEffect(() => {
    if (!sending) {
      setText("");
    }
  }, [sending]);

  function sendMessage() {
    setSending(true);
    sendClientMessage(socket.current, text);
  }

  function sendEnterMessage(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (!e.shiftKey && e.key === "Enter" && text.length > 0) {
      sendMessage();
      // resetHeight();
    } else {
      const el = e.target as HTMLTextAreaElement;
      const style = textAreaRef.current!.style;
      adjustHeight(style, el);
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-input">
        <textarea
          className="chat-textarea"
          aria-invalid="false"
          autoComplete="false"
          id="chat-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your message here and press ENTER..."
          onKeyUp={sendEnterMessage}
          disabled={sending || !connected}
          ref={textAreaRef}
        />
        <button onClick={e => {
          e.preventDefault();
          sendMessage();
        }}>
          <img src="send_button.svg" alt="Send" />
        </button>
      </div>
    </div>
  );
}
