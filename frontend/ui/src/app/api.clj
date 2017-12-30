(ns app.api
  (:require [castra.core :refer [defrpc]])
  (:require [clj-http.client :as client])
  (:require [clojure.data.json :as json]))
  ; (:require [app.db :refer [get-all-ws-from-env env-to-sql-hostname]]))





(def graphql-url "http://dmip:5050/graphql")

(defn graphql
  [query]
  (let [response (client/post graphql-url {:body query :content-type :json})
        data (get (get (json/read-str (:body response)) "data") "query")]
    data))
  ; (:body (client/post graphql-url {:body query :content-type :json})))

(defrpc get-nodule-list []
  ; (let [nodules {"abc123" "balcony" "def456" "living room" "ghi789" "kitchen" "jkl012" "bedroom"}])
  (let [nodules ["abc123" "def456" "ghi789" "jkl012"]
        query "{ \"query\": \"{query{allNodules{nodes{name, uid}}}}\"}"
        data (graphql query)]
  ; (let [nodules [{:uid "abc123" :name "balcony"} {:uid "def456" :name "living room"} {:uid "ghi789" :name "kitchen"} {:uid "jkl012" :name "bedroom"}]]
    ; (prn (client/post "http://dmip:5050/graphql" {:data query}))
    (prn data)
    (prn nodules)
    nodules))
