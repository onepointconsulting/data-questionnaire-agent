import { useContext } from "react";
import { AppContext } from "../context/AppContext.tsx";

function SingleNode({
  i,
  covered,
  expectedNodes,
}: {
  i: number;
  covered: boolean;
  expectedNodes: number;
}) {
  return (
    <>
      <div key={`node_${i}`} className={`node ${covered ? "active" : ""}`}>
        {i}
      </div>
      {i !== expectedNodes - 1 && <div className="connector"></div>}
    </>
  );
}

export default function NodeNavigation() {
  const { expectedNodes, messages } = useContext(AppContext);
  return (
    <div className="node-container">
      {[...Array(expectedNodes).keys()].map((i) => {
        const covered = messages.length > i;
        return (
          <SingleNode
            expectedNodes={expectedNodes}
            covered={covered}
            i={i}
            key={`node_${i}`}
          />
        );
      })}
    </div>
  );
}
