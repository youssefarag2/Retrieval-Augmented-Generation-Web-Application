import { Outlet } from 'react-router-dom'
// Components
import RootNav from '../components/RootNav.tsx'
import Main from '../components/Main.tsx'

const ChatLayout = () => {
    return (
        <>
            <RootNav />
            <Main>
                <Outlet />
            </Main>
        </>
    )
}

export default ChatLayout
