import { useContext } from "react";
import { AppContext } from "../context/AppContext.tsx";

function SingleNode({
  i,
  expectedNodes,
}: {
  i: number;
  expectedNodes: number;
}) {
  const {messages, currentMessage, setCurrentMessage} = useContext(AppContext);
  const covered = messages.length > i;
  const connectorCovered = messages.length > i + 1  ;
  return (
    <>
      <div className={`node ${covered ? "active" : ""} ${currentMessage === i ? "current" : ""}`}>
        {i < messages.length ? <a href="#" onClick={e => {
          e.preventDefault();
          setCurrentMessage(i);
        }}>{i}</a> : i}
      </div>
      {i !== expectedNodes - 1 && <div className={`connector ${connectorCovered ? "active" : ""}`}></div>}
    </>
  );
}

export default function NodeNavigation() {
  const { expectedNodes } = useContext(AppContext);
  return (
    <div className="node-container">
      {[...Array(expectedNodes).keys()].map((i) => {
        return (
          <SingleNode
            expectedNodes={expectedNodes}
            i={i}
            key={`node_${i}`}
          />
        );
      })}
    </div>
  );
}
