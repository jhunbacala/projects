package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"

	"gopkg.in/yaml.v2"
)

var (
	redirects     map[string]string
	mu            sync.RWMutex
	redirectsFile = "redirects.yaml"
)

// loadRedirects reads the YAML file and updates the redirects map.
func loadRedirects() error {
	data, err := ioutil.ReadFile(redirectsFile)
	if err != nil {
		return fmt.Errorf("could not read redirects file: %w", err)
	}

	var newRedirects map[string]string
	if err := yaml.Unmarshal(data, &newRedirects); err != nil {
		return fmt.Errorf("could not parse redirects YAML: %w", err)
	}

	mu.Lock()
	redirects = newRedirects
	mu.Unlock()

	log.Printf("Loaded %d redirect rules.", len(newRedirects))
	return nil
}

// watchRedirectsFile polls the redirects file for changes.
func watchRedirectsFile() {
	var lastModTime time.Time
	for {
		// Use a ticker to avoid a tight loop
		time.Sleep(5 * time.Second)

		info, err := os.Stat(redirectsFile)
		if err != nil {
			log.Printf("Error stating redirects file: %v", err)
			continue
		}

		if info.ModTime().After(lastModTime) {
			log.Println("Redirects file changed, reloading...")
			if err := loadRedirects(); err != nil {
				log.Printf("Error reloading redirects: %v", err)
			}
			lastModTime = info.ModTime()
		}
	}
}

// redirectHandler finds the appropriate redirect and sends the user there.
func redirectHandler(w http.ResponseWriter, r *http.Request) {
	mu.RLock()
	dest, ok := redirects[r.URL.Path]
	mu.RUnlock()

	if !ok {
		http.NotFound(w, r)
		return
	}

	http.Redirect(w, r, dest, http.StatusMovedPermanently)
}

func main() {
	// Initial load of redirects
	if err := loadRedirects(); err != nil {
		log.Fatalf("Failed to perform initial load of redirects: %v", err)
	}

	// Watch for file changes in a separate goroutine
	go watchRedirectsFile()

	http.HandleFunc("/", redirectHandler)

	port := "8080"
	log.Printf("Starting URL redirector on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Could not start server: %s\n", err)
	}
}