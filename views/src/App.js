import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./Pages/Register";
import Login from "./Pages/Login";
import UserTerminal from "./Pages/UserTerminal";
import UserGui from "./Pages/UserGui";
import AdminGui from "./Pages/AdminGui";

function App() {
  return (
    <BrowserRouter>
      <div className="flex w-full h-[100%] items-center justify-center">
        <Routes>
          <Route path="/Register" element={<Register />}></Route>
          <Route path="/Login" element={<Login />}></Route>
          <Route path="/UserTerminal" element={<UserTerminal />}></Route>
          <Route path="/UserGui" element={<UserGui />}></Route>
          <Route path="/" element={<Login />}></Route>
          <Route path="/File-Sharing-UI" element={<Login />}></Route>
          <Route path="/AdminGui" element={<AdminGui />}></Route>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
