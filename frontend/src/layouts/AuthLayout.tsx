import { Outlet } from 'react-router-dom'
// Components
import AuthNav from '../components/AuthNav.tsx'
import Main from '../components/Main.tsx'

const AuthLayout = () => {
    return (
        <>
            <AuthNav />
            <Main>
                <Outlet />
            </Main>
        </>
    )
}

export default AuthLayout
