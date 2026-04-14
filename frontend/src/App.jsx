import { useState } from 'react'
import Home from './pages/Home'
import Result from './pages/Result'

export default function App() {
  const [result, setResult] = useState(null)

  if (result) {
    return <Result data={result} onBack={() => setResult(null)} />
  }

  return <Home onResult={setResult} />
}
