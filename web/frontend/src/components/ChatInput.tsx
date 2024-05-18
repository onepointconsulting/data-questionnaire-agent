import { useContext, useEffect, useRef } from "react";
import { AppContext } from "../context/AppContext.tsx";
import { sendClientMessage } from "../lib/websocketFunctions.ts";
import { ChatContext } from "../context/ChatContext.tsx";

function adjustHeight(style: CSSStyleDeclaration, el: HTMLTextAreaElement) {
  style.height = `auto`;
  style.height = `${el.scrollHeight}px`;
}

function enoughText(chatText: string) {
  return chatText?.length > 2;
}

/**
 * Chat input field to be used in this application.
 * @constructor
 */
export default function ChatInput() {
  const {
    selectedSuggestion,
    setSending,
    sending,
    connected,
    chatText,
    setChatText,
  } = useContext(AppContext);
  const { socket } = useContext(ChatContext);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (selectedSuggestion && textAreaRef.current) {
      setChatText(selectedSuggestion);
    }
  }, [selectedSuggestion]);

  useEffect(() => {
    if (textAreaRef.current) {
      const style = textAreaRef.current.style;
      const el = textAreaRef.current;
      adjustHeight(style, el);
    }
  }, [chatText]);

  useEffect(() => {
    if (!sending) {
      setChatText("");
    }
  }, [sending]);

  function sendMessage() {
    setSending(true);
    sendClientMessage(socket.current, chatText);
  }

  function sendEnterMessage(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (!e.shiftKey && e.key === "Enter" && chatText.length > 0) {
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
          value={chatText}
          onChange={(e) => setChatText(e.target.value)}
          placeholder="Type your message here and press ENTER..."
          onKeyUp={sendEnterMessage}
          disabled={sending || !connected}
          ref={textAreaRef}
        />
        {connected && (
          <button
            onClick={(e) => {
              e.preventDefault();
              sendMessage();
            }}
            disabled={!enoughText(chatText) || sending}
            className="disabled:opacity-10"
          >
            <img
              src="send_button.svg"
              alt="Send"
              title={
                enoughText(chatText)
                  ? "Send message"
                  : "Please enter some text to send"
              }
            />
          </button>
        )}
      </div>
    </div>
  );
}
