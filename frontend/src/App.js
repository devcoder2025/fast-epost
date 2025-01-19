import logo from './logo.svg';
import DragAndDropTemplate from './components/DragAndDropTemplate';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header"> 
        <DragAndDropTemplate />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
