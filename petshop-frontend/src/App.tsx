import { OwnerList } from "./OwnerList";
import { OwnerForm } from "./OwnerForm";
import { PetList } from "./PetList";
import { PetForm } from "./PetForm";
import { useState } from "react";
import {
  RouterProvider,
  createBrowserRouter,
  Outlet,
  NavLink,
} from "react-router-dom";
import "./index.css";

function Layout() {
  return (
    <div
      className="min-h-screen flex flex-col items-center py-8 px-2"
      style={{ background: "var(--ctp-mocha-base)" }}
    >
      <nav className="w-full max-w-3xl mb-8">
        <ul className="flex gap-6 justify-center text-lg font-medium bg-mocha-surface rounded-lg shadow p-4 items-center">
          <li className="mr-6 flex-shrink-0">
            <img
              src="/pet-logo.svg"
              alt="Pet Shop Logo"
              className="h-9 w-9 rounded-full shadow"
              style={{ background: "var(--ctp-mocha-base)" }}
            />
          </li>
          <li>
            <NavLink
              to="/owners"
              className={({ isActive }) =>
                `nav-link${isActive ? " nav-link-active" : ""}`
              }
              end
            >
              Owners List
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/add-owner"
              className={({ isActive }) =>
                `nav-link${isActive ? " nav-link-active" : ""}`
              }
            >
              Add Owner
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/pets"
              className={({ isActive }) =>
                `nav-link${isActive ? " nav-link-active" : ""}`
              }
              end
            >
              Pets List
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/add-pet"
              className={({ isActive }) =>
                `nav-link${isActive ? " nav-link-active" : ""}`
              }
            >
              Add Pet
            </NavLink>
          </li>
        </ul>
      </nav>
      <Outlet />
    </div>
  );
}

function OwnersListRoute() {
  return <OwnerList />;
}
function OwnerFormRoute() {
  const [refresh, setRefresh] = useState(0);
  return <OwnerForm onCreated={() => setRefresh((r) => r + 1)} key={refresh} />;
}
function PetsListRoute() {
  return <PetList />;
}
function PetFormRoute() {
  const [refresh, setRefresh] = useState(0);
  return <PetForm onCreated={() => setRefresh((r) => r + 1)} key={refresh} />;
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { path: "/owners", element: <OwnersListRoute /> },
      { path: "/add-owner", element: <OwnerFormRoute /> },
      { path: "/pets", element: <PetsListRoute /> },
      { path: "/add-pet", element: <PetFormRoute /> },
      { index: true, element: <OwnersListRoute /> },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
