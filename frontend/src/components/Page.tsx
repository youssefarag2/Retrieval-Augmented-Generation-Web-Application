// Types
import { PageProps } from '../types/Types.ts'
// Style
import '../styles/components/Page.css'

const Page = ({ id, children }: PageProps) => {
    return (
        <div id={id} className='page'>
            {children}
        </div>
    )
}

export default Page
