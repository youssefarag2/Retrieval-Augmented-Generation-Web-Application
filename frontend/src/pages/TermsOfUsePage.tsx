// Components
import Page from '../components/Page.tsx'
// Style
import '../styles/pages/TermsAndPrivacyPages.css'

const TermsOfUsePage = () => {
    return (
        <Page id='terms-of-use-page'>
            <h1>{'Terms of Use'.toUpperCase()}</h1>
            <ul>
                {/* 1 */}
                <li className='ul-child'>Acceptance of Terms</li>
                <p>
                    By accessing and using FCDS Mentor, you agree to comply with
                    these Terms of Use. If you do not agree with any part of
                    these terms, you should discontinue using the website
                    immediately. These terms apply to all visitors, users, and
                    others who access or use the service.
                </p>
                {/* 2 */}
                <li className='ul-child'>Purpose of the Website</li>
                <p>
                    FCDS Mentor is designed to provide AI-generated answers
                    related to the Faculty of Computing and Data Science (FCDS).
                    While we strive to provide accurate and helpful responses,
                    the information is based on available data and AI
                    algorithms. The website does not replace official academic
                    advice, university policies, or guidance from authorized
                    faculty members.
                </p>
                {/* 3 */}
                <li className='ul-child'>User Responsibilities</li>
                <p>As a user of FCDS Mentor, you agree to:</p>
                <ol>
                    <li>
                        Use the website for educational and informational
                        purposes only.
                    </li>
                    <li>
                        Not engage in any activity that could harm, disrupt, or
                        manipulate the service, such as attempting to exploit
                        vulnerabilities or overload the system.
                    </li>
                    <li>
                        Not use the AI-generated responses for any illegal or
                        unethical activities.
                    </li>
                    <li>
                        Understand that all information provided is AI-generated
                        and should be verified from official sources when
                        necessary.
                    </li>
                </ol>
                {/* 4 */}
                <li className='ul-child'>Intellectual Property</li>
                <p>
                    All content, including but not limited to text, graphics,
                    logos, and AI-generated responses, belongs to FCDS Mentor
                    unless otherwise stated. You may not copy, distribute,
                    modify, or create derivative works based on the website’s
                    content without prior written permission.
                </p>
                {/* 5 */}
                <li className='ul-child'>Limitation of Liability</li>
                <ol>
                    <li>
                        FCDS Mentor does not guarantee that all answers provided
                        will be accurate, up-to-date, or suitable for all
                        purposes.
                    </li>
                    <li>
                        We are not responsible for any direct or indirect
                        damages resulting from the use of the website, including
                        errors in information or decisions made based on
                        AI-generated responses.
                    </li>
                    <li>
                        The service may experience occasional downtime due to
                        updates, maintenance, or unforeseen technical issues.
                    </li>
                </ol>
                {/* 6 */}
                <li className='ul-child'>
                    External Links and Third-Party Content
                </li>
                <p>
                    The website may include links to external sources for
                    further reference. We do not endorse, control, or take
                    responsibility for the accuracy or reliability of
                    third-party websites. Visiting external links is at your own
                    risk.
                </p>
                {/* 7 */}
                <li className='ul-child'>Changes to Terms</li>
                <p>
                    We reserve the right to update or modify these Terms of Use
                    at any time without prior notice. Users are encouraged to
                    review this page periodically. Continued use of the website
                    after changes are posted constitutes acceptance of the new
                    terms.
                </p>
                {/* 8 */}
                <li className='ul-child'>Termination of Access</li>
                <p>
                    FCDS Mentor reserves the right to terminate or restrict
                    access to users who violate these terms or misuse the
                    website.
                </p>
            </ul>
        </Page>
    )
}

export default TermsOfUsePage
