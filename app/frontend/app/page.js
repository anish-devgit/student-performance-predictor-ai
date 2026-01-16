import PredictorForm from '../components/PredictorForm';
import ThemeToggle from '../components/ThemeToggle';
import styles from './page.module.css';
import { FaGithub, FaHeart } from 'react-icons/fa';

export default function Home() {
  return (
    <main className={styles.main}>
      <ThemeToggle />
      <div className={styles.hero}>
        <h1 className={styles.title}>Student Performance <span className={styles.highlight}>AI</span></h1>
        <p className={styles.subtitle}>
          Predict your final exam score with advanced machine learning based on your habits and background.
        </p>
      </div>
      <PredictorForm />

      <footer className={styles.footer}>
        <p className={styles.credit}>
          Made with <FaHeart className={styles.heartIconSmall} /> by <strong>Anish Raj</strong>
        </p>
        <div className={styles.links}>
          <a 
            href="https://github.com/anish-devgit/student-performance-predictor-ai" 
            target="_blank" 
            rel="noopener noreferrer" 
            className={styles.socialLink}
          >
             <FaGithub /> Star on GitHub
          </a>
          <a 
            href="https://github.com/sponsors/anish-devgit" 
            target="_blank" 
            rel="noopener noreferrer" 
            className={`${styles.socialLink} ${styles.sponsor}`}
          >
             <FaHeart className={styles.heartIcon} /> Sponsor Me
          </a>
        </div>

      </footer>

    </main>
  );
}
