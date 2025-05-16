import {
    Route,
    RouterProvider,
    createBrowserRouter,
    createRoutesFromChildren,
} from 'react-router-dom'
// Layouts
import RootLayout from './layouts/RootLayout.tsx'
import AuthLayout from './layouts/AuthLayout.tsx'
import ChatLayout from './layouts/ChatLayout.tsx'
// Pages
import HomePage from './pages/HomePage.tsx'
import AboutPage from './pages/AboutPage.tsx'
import LoginPage from './pages/auth/LoginPage.tsx'
import SignupPage from './pages/auth/SignupPage.tsx'
import UploadPage from './pages/UploadPage.tsx'
import BroadcastPage from './pages/BroadcastPage.tsx'
import ChatPage from './pages/chat/ChatPage.tsx'
import TermsOfUsePage from './pages/TermsOfUsePage.tsx'
import PrivacyPolicyPage from './pages/PrivacyPolicyPage.tsx'
import PageNotFoundPage from './pages/PageNotFoundPage.tsx'
// Providers
import { ChatProvider, UserProvider } from './providers/Providers.tsx'
// Style
import './styles/App.css'

const router = createBrowserRouter(
    createRoutesFromChildren(
        <>
            <Route path='/' element={<RootLayout />}>
                <Route index element={<HomePage />} />
                <Route path='about' element={<AboutPage />} />
                <Route path='upload' element={<UploadPage />} />
                <Route path='broadcast' element={<BroadcastPage />} />
                <Route path='privacy-policy' element={<PrivacyPolicyPage />} />
                <Route path='terms-of-use' element={<TermsOfUsePage />} />
                <Route path='*' element={<PageNotFoundPage />} />
            </Route>
            <Route path='auth' element={<AuthLayout />}>
                <Route path='login' element={<LoginPage />} />
                <Route path='signup' element={<SignupPage />} />
                <Route path='*' element={<PageNotFoundPage />} />
            </Route>
            <Route path='chat' element={<ChatLayout />}>
                <Route index element={<ChatPage />} />
                <Route path='*' element={<PageNotFoundPage />} />
            </Route>
        </>
    )
)

const App = () => {
    return (
        <ChatProvider>
            <UserProvider>
                <RouterProvider router={router} />
            </UserProvider>
        </ChatProvider>
    )
}

export default App
