import { useState, useEffect } from "react";
import {
  login,
  fetchBookmarks,
  createBookmark,
  deleteBookmark,
} from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const [bookmarks, setBookmarks] = useState([]);
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");

  // =========================
  // 初期ロード
  // =========================
  useEffect(() => {
    if (loggedIn) {
      loadBookmarks();
    }
  }, [loggedIn]);

  const loadBookmarks = async () => {
    try {
      const data = await fetchBookmarks();
      setBookmarks(data);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================
  // ログイン
  // =========================
  const handleLogin = async () => {
    try {
      await login(email, password);
      setLoggedIn(true);
    } catch (err) {
      alert(err.message);
    }
  };

  // =========================
  // ログアウト
  // =========================
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setLoggedIn(false);
    setBookmarks([]);
  };

  // =========================
  // 作成
  // =========================
  const handleCreate = async () => {
    if (!title || !url) return;

    try {
      const newBookmark = await createBookmark({ title, url });
      setBookmarks([...bookmarks, newBookmark]);
      setTitle("");
      setUrl("");
    } catch (err) {
      alert(err.message);
    }
  };

  // =========================
  // 削除
  // =========================
  const handleDelete = async (id) => {
    try {
      await deleteBookmark(id);
      setBookmarks(bookmarks.filter((b) => b.id !== id));
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      {!loggedIn ? (
        <div>
          <h2>Login</h2>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <br />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <br />
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <div>
          <h2>Bookmarks</h2>

          <button onClick={handleLogout}>Logout</button>

          <hr />

          <h3>Create Bookmark</h3>
          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <br />
          <input
            placeholder="URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <br />
          <button onClick={handleCreate}>Add</button>

          <hr />

          <ul>
            {bookmarks.map((b) => (
              <li key={b.id}>
                {b.title} - {b.url}
                <button
                  style={{ marginLeft: "10px" }}
                  onClick={() => handleDelete(b.id)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;