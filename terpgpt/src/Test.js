import { waveform } from 'ldrs'

waveform.register()

// Default values shown


function App() {
    return (
      <div className="App">
        <l-waveform
            size="35"
            stroke="3.5"
            speed="1" 
            color="black" 
        ></l-waveform>
      </div>
    );
  }

export default App;
  