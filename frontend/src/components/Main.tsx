import { PropsWithChildren } from 'react'
// Components
import Container from './Container.tsx'
// Style
import '../styles/components/Main.css'

const Main = ({ children }: PropsWithChildren) => {
    return (
        <main>
            <Container>{children}</Container>
        </main>
    )
}

export default Main
