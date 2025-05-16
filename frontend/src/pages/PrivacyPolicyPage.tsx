// Components
import Page from '../components/Page.tsx'
// Style
import '../styles/pages/TermsAndPrivacyPages.css'

const PrivacyPolicyPage = () => {
    return (
        <Page id='privacy-policy-page'>
            <h1>{'Privacy Policy'.toUpperCase()}</h1>
            <ul>
                {/* 1 */}
                <li className='ul-child'>Information We Collect</li>
                <p>
                    FCDS Mentor does not require users to create accounts or
                    provide personal details. However, we may collect:
                </p>
                <ol>
                    <li>
                        <strong>Technical Data:</strong> Such as IP addresses,
                        device type, browser version, and browsing behavior to
                        improve website performance.
                    </li>
                    <li>
                        <strong>Usage Data:</strong> Pages visited, time spent
                        on the site, and interaction patterns to analyze how
                        users engage with the platform.
                    </li>
                </ol>
                <p>
                    We do not collect sensitive personal information, such as
                    names, emails, or financial details.
                </p>
                {/* 2 */}
                <li className='ul-child'>
                    How We Use the Collected Information
                </li>
                <p>
                    The information we collect is used solely to enhance the
                    functionality of FCDS Mentor, including:
                </p>
                <ol>
                    <li>Improving AI-generated responses.</li>
                    <li>
                        Monitoring website performance and fixing potential
                        issues.
                    </li>
                    <li>
                        Understanding user preferences to provide a better
                        experience.
                    </li>
                </ol>
                <p>
                    We do not sell, trade, or share user data with third
                    parties.
                </p>
                {/* 3 */}
                <li className='ul-child'>Cookies and Tracking Technologies</li>
                <p>
                    FCDS Mentor may use cookies and similar technologies to
                    enhance the user experience. Cookies help us:
                </p>
                <ol>
                    <li>Recognize returning users and save preferences.</li>
                    <li>Analyze traffic and improve website usability.</li>
                    <li>Detect and prevent fraudulent activities.</li>
                </ol>
                <p>
                    Users can disable cookies through their browser settings,
                    but doing so may affect certain functionalities of the
                    website.
                </p>
                {/* 4 */}
                <li className='ul-child'>Data Security Measures</li>
                <p>
                    We take reasonable steps to protect collected data from
                    unauthorized access, alteration, or destruction. However, no
                    method of data transmission over the internet is 100%
                    secure, and we cannot guarantee absolute protection.
                </p>
                {/* 5 */}
                <li className='ul-child'>Third-Party Services</li>
                <p>
                    FCDS Mentor may integrate third-party tools, such as
                    analytics services, to improve website performance. These
                    services may have their own privacy policies, and we
                    encourage users to review them when interacting with
                    external services.
                </p>
                {/* 6 */}
                <li className='ul-child'>Retention of Data</li>
                <p>
                    We retain usage data for analysis and service improvement
                    but do not keep identifiable user information for extended
                    periods. Retained data is used strictly for internal
                    improvements.
                </p>
                {/* 7 */}
                <li className='ul-child'>Children’s Privacy</li>
                <p>
                    FCDS Mentor is intended for general audiences and does not
                    knowingly collect data from users under 13 years old. If we
                    become aware that a child has provided personal information,
                    we will take steps to remove it.
                </p>
                {/* 8 */}
                <li className='ul-child'>Changes to This Policy</li>
                <p>
                    We may update this Privacy Policy from time to time to
                    reflect changes in data practices. Users are encouraged to
                    check this page periodically for updates. Continued use of
                    the website after changes are posted indicates acceptance of
                    the updated policy.
                </p>
            </ul>
        </Page>
    )
}

export default PrivacyPolicyPage
