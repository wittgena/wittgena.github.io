---
title: "고속 상품 검색을 위한 인덱싱 전략 비교와 실전 선택"
date: 2025-04-11T00:00:00-05:00
categories:
  - Blog
  - Backend
tags:
  - OpenSearch
  - Indexing
---

본 문서는 고속 상품 검색 시스템 설계에서 고려한 다섯 가지 핵심 인덱싱 전략을 비교하고, 실제 시스템에 도입한 방식의 선택 이유를 분석한다. 각 전략은 대용량 트래픽과 실시간성 요구를 만족시키기 위해 분리된 목적과 맥락을 가지고 있으며, 주요 정보 출처와 실전 적용 사례를 포함해 서술한다.

---

## 1. item-index vs hot-index 분리 패턴

### 개요
상품의 정적 정보(`title`, `category`, `brand`)와 실시간 변동 필드(`price`, `stock`)를 분리하여 운영하는 구조. 변경이 잦은 필드는 별도 인덱스(`hot-index`)에서 관리하며, 정적 인덱스(`item-index`)는 검색에 활용된다.

### 장점
- write 부하를 분산하여 OpenSearch 성능 개선
- `item-index`는 변경이 적어 segment merge 비용이 낮음
- `hot-index`는 TTL 및 경량 구조로 유지 가능

### 단점
- 검색 시 `price/stock` 실시간 반영이 어렵고 join 필요
- 검색 정렬/필터에 사용되는 경우 불일치 발생 우려

### 주요 출처
- [Coupang Tech](https://medium.com/coupang-tech)
- [Elastic 공식 블로그](https://www.elastic.co/blog/)

---

## 2. Dual-Write + Scheduled Merge

### 개요
모든 데이터를 `item-index`와 `hot-index`에 동시에 기록한 후, 일정 간격으로 병합하여 검색에 사용하는 `merged-index`를 갱신하는 전략.

### 장점
- 검색은 단일 인덱스를 기준으로 수행되어 구조 단순화
- 최신성과 일관성의 균형 확보
- 주기적 병합을 통한 시스템 부하 제어 가능

### 단점
- 병합 로직 추가로 인프라 복잡성 증가
- 최신성이 실시간보다 다소 느릴 수 있음

### 주요 출처
- [Uber Engineering](https://eng.uber.com/)
- [AWS DMS Docs](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.Elasticsearch.html)

---

## 3. Redis ZSET을 검색 pre-filter로 활용

### 개요
OpenSearch에 요청을 보내기 전, Redis의 ZSET을 이용해 가격 범위, 재고 조건 등을 미리 필터링하여 후보 `item_id`만 전달하는 구조.

### 장점
- OpenSearch 부하 감소 및 응답 속도 향상
- 인메모리 조건 필터링으로 실시간성 강화

### 단점
- Redis 데이터 일관성 유지 필요
- 캐시 무효화 정책 및 동기화 로직 필요

### 주요 출처
- [Redis 공식 문서](https://redis.io/docs/latest/)
- 실무 아키텍처 경험 기반 (비공식)

---

## 4. OpenSearch Refresh 전략 세분화

### 개요
OpenSearch의 `refresh_interval` 및 `replicas` 설정을 상황에 맞게 세분화하여 write 성능을 향상시키는 전략.

### 장점
- 인덱싱 시 write 성능 극대화
- refresh 조정으로 segment merge 빈도 조절 가능

### 단점
- 검색 반영 지연 가능성 존재
- 설정 오류 시 데이터 손실 또는 지연 문제 발생 가능

### 주요 출처
- [OpenSearch 공식 문서](https://opensearch.org/docs/latest/)
- [Elastic Performance Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html)

---

## 5. Kafka CDC + Bulk 병합 인덱싱 구조

### 개요
Debezium, Kafka Streams 등을 통해 DB 변경 이벤트를 수집하고, 이를 OpenSearch에 Bulk 형태로 병합 인덱싱하는 구조.

### 장점
- 변경 이력 기반으로 정확한 병합 가능
- write TPS가 높은 환경에서 병렬 처리로 대응 가능

### 단점
- Kafka 인프라 및 CDC 구성의 복잡도 존재
- 오더 보장과 중복 처리 로직 필요

### 주요 출처
- [Debezium](https://debezium.io/)
- [Confluent OpenSearch Sink](https://docs.confluent.io/cloud/current/connectors/cc-opensearch-sink.html)

---

## 🧭 내가 선택한 전략과 그 이유

나는 **"Dual-Write + Scheduled Merge"** 전략을 선택했다. 이유는 다음과 같다:

1. 검색 API가 단일 인덱스를 기준으로 동작해야 하며, 실시간성과 검색 일관성의 균형이 중요했기 때문
2. 가격/재고 정보는 수 초 단위의 딜레이가 허용되므로 실시간성이 완전 필수는 아님
3. Kafka 기반 병합 파이프라인은 추후 확장성 확보를 고려한 설계였음

이를 통해 높은 검색 일관성, 낮은 OpenSearch 부하, 유연한 병합 주기를 동시에 만족하는 구조를 구현할 수 있었다.

---

## 📚 주요정보출처

| 패턴 | 주요 출처 | 상세 설명 |
|------|-----------|-----------|
| **1. item-index vs hot-index 분리** | 🔹 [Elastic 공식 블로그](https://www.elastic.co/blog/), 🔹 [Coupang 기술 블로그](https://medium.com/coupang-tech) | Lucene 기반 인덱스가 자주 업데이트될 때 segment merge 비용이 커진다는 점을 활용한 분리 전략. 공식 문서보다는 대형 커머스의 운영 전략에서 관찰됨 |
| **2. Dual-Write + Scheduled Merge** | 🔹 [Uber Engineering](https://eng.uber.com/), 🔹 [Pinterest Engineering](https://medium.com/@Pinterest_Engineering), 🔹 AWS DMS 사례 | 실시간성과 검색일관성 간 타협을 위한 전략. CDC 또는 Kafka 기반 병합이 주로 사용되며, 대형 플랫폼에서 비동기 병합 전략으로 채택 |
| **3. Redis ZSET 검색 pre-filter** | 🔹 [Redis 공식 문서](https://redis.io/docs/latest/), 🔹 실무자 블로그 및 RedisConf 발표 | OpenSearch 이전 필터링을 Redis에서 수행함으로써 I/O 비용을 줄이고 빠른 사용자 응답 확보. Sorted Set을 활용한 price range 필터링이 전형적 |
| **4. OpenSearch refresh 전략 세분화** | 🔹 [OpenSearch 공식 문서](https://opensearch.org/docs/latest/), 🔹 Elastic Performance Tuning 문서 | `refresh_interval`과 `number_of_replicas`를 indexing 시점에 조절하여 write performance 향상. Segment merge를 줄이는 것이 핵심 |
| **5. Kafka CDC + bulk 병합 인덱싱** | 🔹 [Debezium + Kafka Connect](https://debezium.io/), 🔹 [Confluent OpenSearch Sink](https://docs.confluent.io/cloud/current/connectors/cc-opensearch-sink.html), 🔹 실전 도입 사례 (e.g., Instacart, Wix) | Kafka 기반 CDC 파이프라인에서 변경 이벤트를 수집하고, 주기적으로 OpenSearch에 bulk write. Stream-to-index 구조로 많이 활용됨 |
# 