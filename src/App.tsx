import "./App.css";
import { AppContextProvider } from "./context/AppContext.tsx";
import CompanionParent from "./components/CompanionParent.tsx";
import { ConfigContextProvider } from "./context/ChatContext.tsx";

function App() {
  return (
    <AppContextProvider>
      <ConfigContextProvider>
        <CompanionParent />
      </ConfigContextProvider>
    </AppContextProvider>
  );
}

export default App;
