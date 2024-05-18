import NodeNavigation from "./NodeNavigation.tsx";
import { useWebsocket } from "../hooks/useWebsocket.ts";
import { useContext, useEffect } from "react";
import { AppContext } from "../context/AppContext.tsx";
import InteractionPanel from "./InteractionPanel.tsx";
import StartButton from "./buttons/StartButton.tsx";
import RestartDialogue from "./dialogue/RestartDialogue.tsx";
import EmailDialogue from "./dialogue/EmailDialogue.tsx";
import Disclaimer from "./Disclaimer.tsx";
import InfoButton from "./buttons/InfoButton.tsx";
import InfoDialogue from "./dialogue/InfoDialogue.tsx";
import RegistrationMessage from "./RegistrationMessage.tsx";
import useChatHistory from "../hooks/useChatHistory.ts";

function ConnectionStatus() {
  const { connected } = useContext(AppContext);

  return (
    <div className="connection-status">
      {connected ? "connected" : "disconnected"}
    </div>
  );
}
export default function CompanionParent() {
  const { setStartSession, displayRegistrationMessage } =
    useContext(AppContext);
  useChatHistory();
  useEffect(() => {
    setStartSession(true);
  }, []);
  useWebsocket();
  return (
    <>
      <RestartDialogue />
      <EmailDialogue />
      <InfoDialogue />
      <div className="header">
        <div className="header-container">
          <h1>
            Onepoint Data Wellness Companion™{" "}
            <span className="experimental">Experimental</span>
          </h1>
          <div className="flex flex-col items-center">
            <div className="flex flex-row items-center cursor-pointer">
              <InfoButton />
              <StartButton />
            </div>
            <ConnectionStatus />
          </div>
        </div>
      </div>
      <NodeNavigation />
      {displayRegistrationMessage && <RegistrationMessage />}
      {!displayRegistrationMessage && <InteractionPanel />}
      <Disclaimer />
    </>
  );
}
