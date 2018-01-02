
(ns app.api
  (:require [castra.core :refer [defrpc]])
  (:require [clj-http.client :as client])
  (:require [clojure.data.json :as json]))
  ; (:require [app.db :refer [get-all-ws-from-env env-to-sql-hostname]]))



(defn recget
  [keys data]
  (reduce #(get %1 %2) data keys))

(def graphql-url "http://dmip:5050/graphql")

(defn make-query
  [params]
  "body")

(defn graphql
  [query]
  (let [response (client/post graphql-url {:body query :content-type :json})
        data (recget ["data" "query"] (json/read-str (:body response)))]
    data))
  ; (:body (client/post graphql-url {:body query :content-type :json})))

(defrpc get-nodule-list []
  ; (let [nodules {"abc123" "balcony" "def456" "living room" "ghi789" "kitchen" "jkl012" "bedroom"}])
  (let [query2 "{ \"query\": \"{query{allNodules{nodes{name, uid}}}}\"}"
        query "{ \"query\": \"{query {allNodules {nodes {name,uid,presence,zoneByZone{name},jobsByNodule{totalCount},componentsByNodule{totalCount}}}}}\"}"
        data (recget ["allNodules" "nodes"] (graphql query))]
    (prn data)
    data))


(defrpc all-nodule-stats []
  (let [data (map #(assoc %1 "num-sensors" 2 "num-actuators" 4 "num-jobs" 4) (get-nodule-list))]
    (prn data)
    data))
