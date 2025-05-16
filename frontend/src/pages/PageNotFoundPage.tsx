import { Link } from 'react-router-dom'
// Components
import Page from '../components/Page.tsx'
// Style
import '../styles/pages/PageNotFoundPage.css'

const PageNotFoundPage = () => {
    return (
        <Page id='page-not-found-page'>
            <div>
                <h1>{'Error 404'.toUpperCase()}</h1>
                <h3>{'Page Not Found'.toUpperCase()}</h3>
            </div>
            <Link to='/'>Back To Home</Link>
        </Page>
    )
}

export default PageNotFoundPage
