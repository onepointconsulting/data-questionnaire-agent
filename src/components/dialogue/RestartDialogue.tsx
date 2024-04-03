import {useContext, useState} from "react";
import { clearSession } from "../../lib/sessionFunctions.ts";
import { sendStartSession } from "../../lib/websocketFunctions.ts";
import { ChatContext } from "../../context/ChatContext.tsx";
import {AppContext} from "../../context/AppContext.tsx";

export const RESTART_DIALOGUE_ID = "restart-dialogue";

function onClose() {
  const myDialog: any | null = document.getElementById(RESTART_DIALOGUE_ID);
  if (myDialog) {
    myDialog.close();
  }
}

export default function RestartDialogue() {
  const { socket } = useContext(ChatContext);
  const { expectedNodes } = useContext(AppContext);
  const [expectedInteviewSteps, setExpectedInterviewSteps] = useState(expectedNodes);

  function onOk() {
    clearSession();
    sendStartSession(socket.current, expectedInteviewSteps);
    onClose();
  }

  return (
    <dialog
      data-model={true}
      id={RESTART_DIALOGUE_ID}
      className="companion-dialogue"
    >
      <div className="companion-dialogue-content">
        Would you like to restart the companion?
      </div>
      <div className="companion-dialogue-config">
        <label htmlFor="expectedInteviewSteps">Interview Steps: </label>
        <input id="expectedInteviewSteps" type="number" min={4} max={7} value={expectedInteviewSteps}
               onChange={(e) => setExpectedInterviewSteps(parseInt(e.target.value))} />
      </div>
      <div className="companion-dialogue-buttons">
        <button
          data-close-modal={true}
          onClick={onClose}
          className="button-cancel"
        >
          Close
        </button>
        <button data-close-modal={true} onClick={onOk} className="button-ok">
          OK
        </button>
      </div>
    </dialog>
  );
}
