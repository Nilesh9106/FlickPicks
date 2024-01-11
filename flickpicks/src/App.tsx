
import { RouterProvider, createBrowserRouter, redirect } from "react-router-dom"
import Header from "./components/Navbar"
import Auth from "./pages/auth/auth"
import Home from "./pages/home/home"
import { ToastContainer } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css';
import "react-multi-carousel/lib/styles.css";
import Favorites from "./pages/favorites/Favorites"
import History from "./pages/history/History"
import Movie from "./pages/movie/Movie"
import Search from "./pages/search/Search"

const router = createBrowserRouter([
  {
    path: '/',
    element: <Header />,
    loader: async () => {
      if (!localStorage.getItem("token")) {
        return redirect("/auth")
      }
      return null
    },
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: 'favorites',
        element: <Favorites />
      },
      {
        path: 'history',
        element: <History />
      },
      {
        path: 'movie/:id',
        element: <Movie />
      },
      {
        path : 'search',
        element: <Search />
      }
    ]
  },
  {
    path: '/auth',
    element: <Auth />,
    loader: async () => {
      if (localStorage.getItem("token")) {
        return redirect("/")
      }
      return null
    }
  }
])

function App() {
  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
      />
      <RouterProvider router={router} />
    </>
  )
}

export default App
