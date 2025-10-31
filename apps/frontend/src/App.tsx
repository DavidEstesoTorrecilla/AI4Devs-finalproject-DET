import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </Router>
  );
}

// Temporary placeholder components
function HomePage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-primary mb-4">EMASAI</h1>
        <p className="text-muted-foreground mb-8">
          Sistema de Monitoreo y Gestión de Máquinas Industriales
        </p>
        <a
          href="/login"
          className="inline-flex items-center justify-center px-6 py-3 text-white bg-primary rounded-md hover:bg-primary/90"
        >
          Iniciar Sesión
        </a>
      </div>
    </div>
  );
}

function LoginPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md p-8 space-y-6 bg-card rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-center">Iniciar Sesión</h2>
        <p className="text-center text-muted-foreground">
          Login page - To be implemented
        </p>
      </div>
    </div>
  );
}

function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <p className="text-muted-foreground">Dashboard - To be implemented</p>
    </div>
  );
}

function NotFoundPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary mb-4">404</h1>
        <p className="text-xl text-muted-foreground mb-8">Página no encontrada</p>
        <a href="/" className="text-primary hover:underline">
          Volver al inicio
        </a>
      </div>
    </div>
  );
}

export default App;
