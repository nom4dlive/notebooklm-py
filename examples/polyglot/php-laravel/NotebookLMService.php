<?php

namespace App\Services;

use Exception;

/**
 * Class NotebookLMService
 *
 * Polyglot Client Service for Google NotebookLM via notebooklm-py REST Server.
 * Usable inside Laravel applications or standalone PHP (PHP 8.1+).
 */
class NotebookLMService
{
    protected string $baseUrl;
    protected string $profile;
    protected int $timeout;

    public function __construct(?string $baseUrl = null, ?string $profile = null, int $timeout = 60)
    {
        $this->baseUrl = rtrim($baseUrl ?? (function_exists('config') ? config('services.notebooklm.url', 'http://127.0.0.1:8000/v1') : 'http://127.0.0.1:8000/v1'), '/');
        $this->profile = $profile ?? (function_exists('config') ? config('services.notebooklm.profile', 'default') : 'default');
        $this->timeout = $timeout;
    }

    /**
     * Internal HTTP request dispatcher using cURL.
     *
     * @param string $endpoint
     * @param string $method
     * @param array|null $payload
     * @return array
     * @throws Exception
     */
    protected function request(string $endpoint, string $method = 'GET', ?array $payload = null): array
    {
        $url = $this->baseUrl . '/' . ltrim($endpoint, '/');
        $ch = curl_init($url);

        $headers = [
            'Content-Type: application/json',
            'Accept: application/json',
            'X-NotebookLM-Profile: ' . $this->profile,
        ];

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_TIMEOUT, $this->timeout);

        if ($method === 'POST') {
            curl_setopt($ch, CURLOPT_POST, true);
            if ($payload !== null) {
                curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
            }
        } elseif ($method !== 'GET') {
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        }

        $responseBody = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlError = curl_error($ch);
        curl_close($ch);

        if ($curlError) {
            throw new Exception("NotebookLM Connection Error: " . $curlError);
        }

        $decoded = json_decode($responseBody, true);

        if ($httpCode >= 400) {
            $errorMsg = $decoded['message'] ?? $decoded['detail'] ?? $responseBody;
            throw new Exception("NotebookLM API Error [HTTP {$httpCode}]: {$errorMsg}");
        }

        return $decoded ?? [];
    }

    /**
     * List all notebooks available in the active profile.
     *
     * @return array
     * @throws Exception
     */
    public function listNotebooks(): array
    {
        return $this->request('/notebooks', 'GET');
    }

    /**
     * Create a new notebook.
     *
     * @param string $title
     * @return array
     * @throws Exception
     */
    public function createNotebook(string $title): array
    {
        return $this->request('/notebooks', 'POST', [
            'title' => $title,
        ]);
    }

    /**
     * Attach a URL source to a notebook.
     *
     * @param string $notebookId
     * @param string $url
     * @return array
     * @throws Exception
     */
    public function addSourceUrl(string $notebookId, string $url): array
    {
        return $this->request("/notebooks/{$notebookId}/sources", 'POST', [
            'type' => 'url',
            'url' => $url,
        ]);
    }

    /**
     * Ask a question grounded on notebook sources.
     *
     * @param string $notebookId
     * @param string $question
     * @return string
     * @throws Exception
     */
    public function ask(string $notebookId, string $question): string
    {
        $response = $this->request("/notebooks/{$notebookId}/ask", 'POST', [
            'question' => $question,
        ]);

        return $response['answer'] ?? '';
    }
}
