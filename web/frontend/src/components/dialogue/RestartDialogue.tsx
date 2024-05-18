import { useContext, useState } from "react";
import { clearSession } from "../../lib/sessionFunctions.ts";
import { sendStartSession } from "../../lib/websocketFunctions.ts";
import { ChatContext } from "../../context/ChatContext.tsx";
import { AppContext } from "../../context/AppContext.tsx";
import onCloseDialogue from "../../lib/dialogFunctions.ts";
import ButtonPanel from "./ButtonPanel.tsx";
import { ImSwitch } from "react-icons/im";

export const RESTART_DIALOGUE_ID = "restart-dialogue";

const MIN_STEPS = 4;

const MAX_STEPS = 8;

function onClose() {
  onCloseDialogue(RESTART_DIALOGUE_ID);
}

export default function RestartDialogue() {
  const { socket } = useContext(ChatContext);
  const { expectedNodes, messages, setDisplayRegistrationMessage } =
    useContext(AppContext);
  const [expectedInteviewSteps, setExpectedInterviewSteps] =
    useState(expectedNodes);

  function onOk() {
    clearSession(messages);
    sendStartSession(
      socket.current,
      expectedInteviewSteps,
      setDisplayRegistrationMessage,
    );
    onClose();
  }

  return (
    <dialog
      data-model={true}
      id={RESTART_DIALOGUE_ID}
      className="companion-dialogue"
    >
      <div className="companion-dialogue-content">
        <h2>
          <ImSwitch className="inline relative -top-1 fill-[#0084d7]" /> Restart
        </h2>
        <section className="mx-3 mt-10">
          <p>Would you like to restart the companion?</p>
          <div className="companion-dialogue-config">
            <label htmlFor="expectedInteviewSteps">Interview Steps: </label>
            <select
              id="expectedInteviewSteps"
              value={expectedInteviewSteps}
              onChange={(e) =>
                setExpectedInterviewSteps(parseInt(e.target.value))
              }
            >
              {Array.from({ length: MAX_STEPS - MIN_STEPS + 1 }, (_, i) => (
                <option key={i} value={i + MIN_STEPS}>
                  {i + MIN_STEPS}
                </option>
              ))}
            </select>
          </div>
        </section>
      </div>

      <ButtonPanel onOk={onOk} onClose={onClose} okText="OK" disabled={false} />
    </dialog>
  );
}
