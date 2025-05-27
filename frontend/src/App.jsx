
import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [city, setCity] = useState('')
  const [loading, setLoading] = useState(false)
  const [events, setEvents] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [selectedLink, setSelectedLink] = useState('')
  const [email, setEmail] = useState('')

  const handleShowEvents = async () => {
    if (!city.trim()) return alert('Please enter a city')
    try {
      setLoading(true)
      const response = await axios.post('https://backend-kappa-lilac-49.vercel.app/api/v1/eventsInCity', { city },
  {
    withCredentials: true,
  })
      setEvents(response?.data?.data)
    } catch (error) {
      alert("Please try again")
      console.error('Error fetching events:', error)
      setEvents([])
    } finally {
      setLoading(false)
    }
  }

  const handleUserEvents = async()=>(setShowModal(true));

  const handleSubmit = async () => {
    try {
      const res = await axios.post('https://backend-kappa-lilac-49.vercel.app/api/v1/addUser', { email });
      
      if(res.data.success===true){
        console.log('Email submitted:', email);
        console.log(selectedLink);
        
        window.open(`https://www.district.in/events/${selectedLink}`, '_blank');
      }
      console.log('Email submitted:', email);
    } catch (error) {
      console.error('Error submitting email:', error);
      alert("Something went wrong. Please try again.");
    } finally {
      setShowModal(false);
      setEmail('');
    }
  }

  


  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold text-blue-700 mb-2 text-center">Welcome to Event Search</h1>
      <p className="text-gray-600 mb-6 text-lg text-center">Find all the events happening in your city.</p>

      <div className="flex flex-col sm:flex-row gap-4 mb-8 w-full max-w-xl">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter your city"
          className="flex-1 px-4 py-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />
        <button
          onClick={handleShowEvents}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition font-medium shadow-md disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Show Events'}
        </button>
      </div>

      {loading ? (
        <h2 className="text-lg text-gray-700">Loading, please wait...</h2>
      ) : (
        <div className="w-full max-w-2xl">
          {
            events
              .filter(data => {
                const { Title, Date_Time, Location, ImageURL } = data
                return Title || Date_Time || Location || ImageURL
              })
              .map((data, index) => (
                <div
                  key={index}
                  className="relative bg-cover bg-center rounded-2xl shadow-lg overflow-hidden text-white mb-6"
                  style={{ backgroundImage: data.Link ? `url(${data.Link})` : 'none' }}
                >
                  <div className="bg-black bg-opacity-60 p-6">
                    {data.Title && <p className="text-2xl font-bold mb-2">🎉 {data.Title}</p>}
                    {data.City && <p className="mb-1">📍 City: {data.City}</p>}
                    {data.Date_Time && <p className="mb-1">📅 Date & Time: {data.Date_Time}</p>}
                    {data.Location && <p className="mb-1">📌 Location: {data.Location}</p>}
                    {data.Price && <p className="mb-1">💰 Price: {data.Price}</p>}
                    {data.ImageURL && (
                      <img
                        src={data.ImageURL}
                        alt="Event"
                        className="mt-4 w-full h-48 object-cover rounded-xl border border-white/20"
                      />
                    )}
                    {data.Link && (
                      <button
                        onClick={() => handleUserEvents(
                          setSelectedLink(data.Link))}
                        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition font-medium shadow-md mt-4"
                      >
                        🎟️ GET TICKETS
                      </button>
                    )}
                  </div>
                </div>
              ))
          }
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md relative">

            <h2 className="text-2xl font-bold mb-4">Get Your Ticket</h2>
            <label className="block mb-2 text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mb-4 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
            />
            <button
              onClick={handleSubmit}
              className="bg-blue-600 text-white w-full py-2 rounded-md hover:bg-blue-700 transition"
            >
              Submit
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
