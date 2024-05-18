import { Location, useLocation } from "react-router-dom";
import { AppContext } from "../context/AppContext.tsx";
import { useContext, useEffect } from "react";

export default function useChatHistory() {
  const location: Location = useLocation();
  const { setCurrentMessage } = useContext(AppContext);
  useEffect(() => {
    const locationIndex = location.pathname.split("/").pop();
    if (locationIndex) {
      setCurrentMessage(parseInt(locationIndex));
    }
  }, [location]);
}
