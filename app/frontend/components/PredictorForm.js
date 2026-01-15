"use client";
import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import styles from '../app/page.module.css';

export default function PredictorForm() {
    const [formData, setFormData] = useState({
        age: 20,
        gender: "male",
        course: "undergraduate",
        study_hours: 5.0,
        class_attendance: 80.0,
        internet_access: "yes",
        sleep_hours: 7.0,
        sleep_quality: "average",
        study_method: "self-study",
        facility_rating: "moderate",
        exam_difficulty: "moderate"
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [featureImportance, setFeatureImportance] = useState([]);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

    useEffect(() => {
        // Fetch feature importance on mount
        fetch(`${API_URL}/feature_importance`)
            .then(res => res.json())
            .then(data => setFeatureImportance(data))
            .catch(err => console.error("Failed to load insights", err));
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: ["age", "study_hours", "class_attendance", "sleep_hours"].includes(name) 
                ? Number(value) 
                : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Prediction failed");
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <form onSubmit={handleSubmit} className={styles.form}>
                <h2 className={styles.sectionTitle}>Student Details</h2>
                
                <div className={styles.grid}>
                    {/* Numeric Fields */}
                    <div className={styles.field}>
                        <label>Age</label>
                        <input type="number" name="age" value={formData.age} onChange={handleChange} min="10" max="100" required />
                    </div>
                    <div className={styles.field}>
                        <label>Study Hours (Daily)</label>
                        <input type="number" step="0.5" name="study_hours" value={formData.study_hours} onChange={handleChange} min="0" max="24" required />
                    </div>
                    <div className={styles.field}>
                        <label>Class Attendance (%)</label>
                        <input type="number" step="1" name="class_attendance" value={formData.class_attendance} onChange={handleChange} min="0" max="100" required />
                    </div>
                    <div className={styles.field}>
                        <label>Sleep Hours (Daily)</label>
                        <input type="number" step="0.5" name="sleep_hours" value={formData.sleep_hours} onChange={handleChange} min="0" max="24" required />
                    </div>

                    {/* Categorical Fields */}
                    <div className={styles.field}>
                        <label>Gender</label>
                        <select name="gender" value={formData.gender} onChange={handleChange}>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Course Level</label>
                        <select name="course" value={formData.course} onChange={handleChange}>
                            <option value="diploma">Diploma</option>
                            <option value="undergraduate">Undergraduate</option>
                            <option value="postgraduate">Postgraduate</option>
                            <option value="phd">PhD</option>
                            <option value="certificate">Certificate</option>
                            <option value="professional">Professional</option>
                            <option value="vocational">Vocational</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Internet Access</label>
                        <select name="internet_access" value={formData.internet_access} onChange={handleChange}>
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Sleep Quality</label>
                        <select name="sleep_quality" value={formData.sleep_quality} onChange={handleChange}>
                            <option value="poor">Poor</option>
                            <option value="average">Average</option>
                            <option value="good">Good</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Study Method</label>
                        <select name="study_method" value={formData.study_method} onChange={handleChange}>
                            <option value="self-study">Self Study</option>
                            <option value="group-study">Group Study</option>
                            <option value="online">Online</option>
                            <option value="coaching">Coaching</option>
                            <option value="tutoring">Tutoring</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Facility Rating</label>
                        <select name="facility_rating" value={formData.facility_rating} onChange={handleChange}>
                            <option value="low">Low</option>
                            <option value="moderate">Moderate</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                    <div className={styles.field}>
                        <label>Exam Difficulty</label>
                        <select name="exam_difficulty" value={formData.exam_difficulty} onChange={handleChange}>
                            <option value="easy">Easy</option>
                            <option value="moderate">Moderate</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
                </div>

                <div className={styles.actions}>
                    <button type="submit" className={styles.predictBtn} disabled={loading}>
                        {loading ? "Calculating..." : "Predict Score"}
                    </button>
                </div>
            </form>

            {error && <div className={styles.error}>{error}</div>}

            {result && (
                <div className={styles.resultCard}>
                    <h3>Predicted Exam Score</h3>
                    <div className={styles.score}>{result.exam_score}</div>
                    <div className={styles.details}>
                        <span className={styles.confidence}>Confidence: {result.confidence_level}</span>
                        <span className={styles.probability}>Pass Prob: {parseInt(result.pass_probability * 100)}%</span>
                    </div>
                </div>
            )}

            {/* Feature Importance Chart */}
            {featureImportance.length > 0 && (
                <div className={styles.chartCard} style={{ marginTop: '2rem', width: '100%', background: 'var(--card-bg)', padding: '2rem', borderRadius: '1rem', border: '1px solid var(--border)' }}>
                    <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', color: 'var(--text-secondary)' }}>
                        What drives higher scores?
                    </h3>
                    <div style={{ width: '100%', height: 300 }}>
                        <ResponsiveContainer>
                            <BarChart data={featureImportance} layout="vertical" margin={{ left: 20 }}>
                                <XAxis type="number" hide />
                                <YAxis type="category" dataKey="feature" width={150} tick={{fill: '#94a3b8', fontSize: 12}} />
                                <Tooltip 
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', color: '#f8fafc' }}
                                    itemStyle={{ color: '#6366f1' }}
                                    cursor={{fill: 'rgba(255,255,255,0.05)'}}
                                />
                                <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                                    {featureImportance.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={index < 3 ? '#6366f1' : '#334155'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            )}
        </div>
    );
}
