import NodeNavigation from "./NodeNavigation.tsx";
import { useWebsocket } from "../hooks/useWebsocket.ts";
import { useContext, useEffect } from "react";
import { AppContext } from "../context/AppContext.tsx";
import InteractionPanel from "./InteractionPanel.tsx";
import StartButton from "./StartButton.tsx";
import RestartDialogue from "./dialogue/RestartDialogue.tsx";

function ConnectionStatus() {
  const { connected } = useContext(AppContext);

  return (
    <div className="connection-status">
      {connected ? "connected" : "disconnected"}
    </div>
  );
}
export default function CompanionParent() {
  const { setStartSession } = useContext(AppContext);
  useEffect(() => {
    setStartSession(true);
  }, []);
  useWebsocket();
  return (
    <>
      <RestartDialogue />
      <div className="header">
        <div className="header-container">
          <h1>Onepoint Data Wellness Companion™</h1>
          <div className="flex flex-col items-center">
            <StartButton />
            <ConnectionStatus />
          </div>
        </div>
      </div>
      <NodeNavigation />
      <InteractionPanel />
    </>
  );
}
