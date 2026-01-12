import { api } from '@/api'


function getMySourceArticles(query = undefined) {
    return api.get(
        '/article/source_articles/',
        {
            withCredentials: true,
            params: query,
        },
    );
}

function getTheSourceArticle(id) {
    return api.get(`/article/source_articles/${id}/`, { withCredentials: true });
}

function createSourceArticle() {
    return api.post(`/article/source_articles/`)
}

function updateSourceArticle(id, title, content) {
    return api.patch(
        `/article/source_articles/${id}/`,
        {
            title: title,
            content: content,
        },
        { withCredentials: true },
    )
}

function submitArticle(id) {
    return api.post(
        `/article/article_actions/${id}/submit/`,
        {},
        { withCredentials: true }
    );
}

function withdrawArticle(id) {
    return api.post(
        `/article/article_actions/${id}/withdraw/`,
        {},
        { withCredentials: true }
    );
}

function approveArticle(id) {
    return api.post(
        `/article/article_actions/${id}/approve/`,
        {},
        { withCredentials: true }
    );
}

function rejectArticle(id) {
    return api.post(
        `/article/article_actions/${id}/reject/`,
        {},
        { withCredentials: true }
    );
}

function unpublishArticle(id) {
    return api.post(
        `/article/article_actions/${id}/unpublish/`,
        {},
        { withCredentials: true }
    );
}

function deleteArticle(id) {
    return api.post(
        `/article/article_actions/${id}/delete/`,
        {},
        { withCredentials: true }
    );
}

function uploadArticleImage(formData) {

    return api.post(
        `/article/source_articles/upload_article_image/`,
        formData,
        {
            headers: { 'Content-Type': 'multipart/form-data' },
            withCredentials: true,
        }
    )
}

function getPendingArticles() {
    return api.get('/article/article_snapshots/pending/', { withCredentials: true });
}

function getThePendingArticle(id) {
    return api.get(`/article/article_snapshots/${id}/`, { withCredentials: true });
}

function getPublishedArticles() {
    return api.get('/article/published_articles/');
}

function getThePublishedArticle(id) {
    return api.get(`/article/published_articles/${id}/`);
}

export {
    getMySourceArticles,
    getTheSourceArticle,
    createSourceArticle,
    updateSourceArticle,
    submitArticle,
    withdrawArticle,
    approveArticle,
    rejectArticle,
    unpublishArticle,
    deleteArticle,
    uploadArticleImage,
    getPendingArticles,
    getThePendingArticle,
    getPublishedArticles,
    getThePublishedArticle,
}
