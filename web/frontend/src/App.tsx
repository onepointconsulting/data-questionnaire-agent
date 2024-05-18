import "./App.css";
import { AppContextProvider } from "./context/AppContext.tsx";
import CompanionParent from "./components/CompanionParent.tsx";
import { ConfigContextProvider } from "./context/ChatContext.tsx";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <AppContextProvider>
      <ConfigContextProvider>
        <Routes>
          <Route path="*" element={<CompanionParent />} />
        </Routes>
      </ConfigContextProvider>
    </AppContextProvider>
  );
}

export default App;
