import { useState } from "react"
import { sensorsAPI } from "../services/api"

const SensorTestInput = () => {
  const [machineId, setMachineId] = useState("")
  const [temperature, setTemperature] = useState("")
  const [vibration, setVibration] = useState("")
  const [load, setLoad] = useState("")
  const [rpm, setRpm] = useState("")
  const [message, setMessage] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()

    const data = {
      machine_id: Number(machineId),
      temperature: Number(temperature),
      vibration: Number(vibration),
      load: Number(load),
      rpm: Number(rpm),
      acoustic_noise: 0  // you can add field if needed
    }

    try {
      await sensorsAPI.push(data)
      setMessage("Test data sent successfully!")
    } catch (error) {
      setMessage("Error sending test data")
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Sensor Test Input</h2>
      
      <form onSubmit={handleSubmit}>
        <label>Machine ID:</label>
        <input value={machineId} onChange={(e) => setMachineId(e.target.value)} required />

        <label>Temperature:</label>
        <input value={temperature} onChange={(e) => setTemperature(e.target.value)} required />

        <label>Vibration:</label>
        <input value={vibration} onChange={(e) => setVibration(e.target.value)} required />

        <label>Load (%):</label>
        <input value={load} onChange={(e) => setLoad(e.target.value)} required />

        <label>RPM:</label>
        <input value={rpm} onChange={(e) => setRpm(e.target.value)} required />

        <button type="submit">Submit Test Data</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  )
}

export default SensorTestInput
