import { Message } from "../model/message.ts";
import React, { useContext } from "react";
import { AppContext } from "../context/AppContext.tsx";

/**
 * Displays the suggestions available on a specific message.
 * @param message
 * @constructor
 */
export default function Suggestions({ message }: { message: Message }) {
  const { setSelectedSuggestion } = useContext(AppContext);

  function handleSelectedSuggestion(e: React.MouseEvent, suggestion: string) {
    e.preventDefault();
    setSelectedSuggestion(suggestion);
  }

  return (
    <div className="suggestions container">
      {message.suggestions.map((suggestion, i) => {
        return (
          <div key={`suggestion_${i}`} className="suggestion">
            <div className="suggestion-img">
              <a
                href={suggestion.title}
                onClick={(e) => handleSelectedSuggestion(e, suggestion.title)}
              >
                <img src={suggestion.img_src} alt={suggestion.img_alt} />
              </a>
            </div>
            <div className="suggestion-text">
              <div>
                <a
                  href={suggestion.title}
                  onClick={(e) =>
                    handleSelectedSuggestion(
                      e,
                      `${suggestion.title} - ${suggestion.main_text}`,
                    )
                  }
                >
                  <b>{suggestion.title}</b> - {suggestion.main_text}
                </a>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
