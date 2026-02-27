// src/api.js
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

// 共通ヘッダー
function getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
}

// =======================
// Auth
// =======================
export async function login(email, password) {
    const res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!res.ok) throw new Error("Login failed");
    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    return data;
}

// =======================
// Bookmarks
// =======================
export async function fetchBookmarks() {
    const res = await fetch(`${BASE_URL}/bookmarks/`, {
        headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch bookmarks");
    return res.json();
}

export async function createBookmark(bookmark) {
    const res = await fetch(`${BASE_URL}/bookmarks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify(bookmark),
    });
    if (!res.ok) throw new Error("Failed to create bookmark");
    return res.json();
}

export async function updateBookmark(id, bookmark) {
    const res = await fetch(`${BASE_URL}/bookmarks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify(bookmark),
    });
    if (!res.ok) throw new Error("Failed to update bookmark");
    return res.json();
}

export async function deleteBookmark(id) {
    const res = await fetch(`${BASE_URL}/bookmarks/${id}`, {
        method: "DELETE",
        headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error("Failed to delete bookmark");
    return res.json();
}

// =======================
// Tags
// =======================
export async function fetchTags() {
    const res = await fetch(`${BASE_URL}/tags/`, {
        headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error("Failed to fetch tags");
    return res.json();
}

export async function createTag(name) {
    const res = await fetch(`${BASE_URL}/tags/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ name }),
    });
    if (!res.ok) throw new Error("Failed to create tag");
    return res.json();
}