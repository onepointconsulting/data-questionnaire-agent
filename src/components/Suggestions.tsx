import { Message } from "../model/message.ts";

/**
 * Displays the suggestions available on a specific message.
 * @param message
 * @constructor
 */
export default function Suggestions({ message }: { message: Message }) {
  return (
    <div className="suggestions container">
      {message.suggestions.map((suggestion, i) => {
        return (
          <div key={`suggestion_${i}`} className="suggestion">
            <b>{suggestion.title}</b> - {suggestion.main_text}
          </div>
        );
      })}
    </div>
  );
}
