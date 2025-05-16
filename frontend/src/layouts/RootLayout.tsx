import { Outlet } from 'react-router-dom'
// Components
import RootNav from '../components/RootNav.tsx'
import Main from '../components/Main.tsx'
import Footer from '../components/Footer.tsx'

const RootLayout = () => {
    return (
        <>
            <RootNav />
            <Main>
                <Outlet />
            </Main>
            <Footer />
        </>
    )
}

export default RootLayout
