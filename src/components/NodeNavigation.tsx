import {useContext} from "react";
import {AppContext} from "../context/AppContext.tsx";
import {FaFlagCheckered} from "react-icons/fa";

function OutputNode({i, totalNodes}: { i: number; totalNodes: number }) {
  if (i === totalNodes - 1) {
    return (
      <FaFlagCheckered className="mx-auto"/>
    );
  }
  return (
    <>
      {i + 1}
    </>
  );
}

function SingleNode({
                      i,
                      expectedNodes,
                    }: {
  i: number;
  expectedNodes: number;
}) {
  const {messages, currentMessage, setCurrentMessage} =
    useContext(AppContext);
  const length = messages.length;
  const covered = length > i;
  const connectorCovered = length > i + 1;
  return (
    <>
      <div
        className={`node ${covered ? "active" : ""} ${currentMessage === i ? "current" : ""}`}
      >
        {i < length ? (
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              setCurrentMessage(i);
            }}
          >
            <OutputNode i={i} totalNodes={expectedNodes}/>
          </a>
        ) : (
          <OutputNode i={i} totalNodes={expectedNodes}/>
        )}
      </div>
      {i !== expectedNodes - 1 && (
        <div className={`connector ${connectorCovered ? "active" : ""}`}></div>
      )}
    </>
  );
}

export default function NodeNavigation() {
  const {expectedNodes} = useContext(AppContext);
  return (
    <div className="node-container">
      {[...Array(expectedNodes).keys()].map((i) => {
        return (
          <SingleNode expectedNodes={expectedNodes} i={i} key={`node_${i}`}/>
        );
      })}
    </div>
  );
}
