(ns mq-test.core
  (:gen-class)
  (:require [clojurewerkz.machine-head.client :as mh]
            [clojure.string :as str]
            [clojure.data.json :as json]))

(def topics ["presence" "logs" "errors" "report" "sensors"])

(defn url_to_topic
  [url]
  (nth (str/split url #"/") 0))

(defn send_to_elk [url payload]
  (let [topic (url_to_topic url)
        nodule_id url]
    (println (format "[%s]:%s -> [ELK ]  %s" url topic (String. payload "UTF-8")))))

(defn send_to_db [url payload]
  (let [topic (url_to_topic url)
        nodule_id url]
    (println (format "[%s]:%s -> [DB  ]  %s" url topic (String. payload "UTF-8")))))

(defn send_to_file [url payload]
  (let [topic (url_to_topic url)
        nodule_id url]
    (println (format "[%s]:%s -> [FILE]  %s" url topic (String. payload "UTF-8")))))

(defn router  ; Given a topic, return a list of handler functions that should be called
  [topic]
  (let [routes {"presence" ["elk" "db"]
                "sensors" ["elk" "file"]
                "logs" ["elk"]
                "errors" ["elk"]
                "report" ["elk" "db"]}
        router {"elk" send_to_elk
                "db" send_to_db
                "file" send_to_file}
        destinations (get routes topic)
        funcs (map #(get router %) destinations)]
    funcs))

(defn handle_delivery
  [^String url _ ^bytes payload]
  (let [topic (url_to_topic url)  ; Get topic as first part of url
        funcs (router topic)]  ; Get list of handler functions based on topic
    (doseq [f funcs]  ; Send to each handler function
      (f url payload))))

(defn subscribe_to_topics  ; Subscribe to all topics in a list
  [conn topics handler]
  (prn "subscribing")
  (doseq [t topics]
    (mh/subscribe conn
                  {(str t "/#") 1}
                  handler)))

(defn presence_msg
  [connected name]
  (json/write-str {"presence" (if connected "Connected" "Disconnected") "node" name}))

(defn -main
  [& args]
  (let [name    "collector"
        conn  (mh/connect "tcp://127.0.0.1:1883" name)]
    (subscribe_to_topics conn topics handle_delivery)
    (mh/publish conn (str "presence/" name) (str (presence_msg true name)))
    (Thread/sleep 15000)
    (prn "disconnecting")
    (mh/disconnect conn)
    (System/exit 0)))
