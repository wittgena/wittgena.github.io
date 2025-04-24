---
title: "GPT로 LEGACY 실시간 트렌드 분석 시스템 리팩토링기"
date: 2025-04-24T02:00:00-05:00
categories:
  - Blog
  - GPT
  - REFACTORING
tags:
  - LLM
  - Reflective AI Use
---

**GPT 기반 DSL을 활용하여 구조적으로 진행한 단계적 리팩토링 기록**이며, "@나.dsl", `+action`, `+critic`, `+탈고` 등의 명령으로 리팩토링을 계획하고 평가하며 발전시켜 나갔던 실험의 결과입니다.
코드는 일부 변경하였습니다.

---

### 🔧 문제 인식: 단일 흐름의 과밀한 책임

Kafka Stream 기반 검색 트렌드 집계 시스템의 중심 함수는 다음과 같았습니다. 이 구조는 기능적으로는 문제없지만, 유지보수성 측면에서 점차 문제가 되었습니다:

```kotlin
@Bean
fun aggregateSearchLog(): Consumer<KTable<String, SearchLogDto>> = Consumer { table ->
    val timeWindow = TimeWindows.ofSizeAndGrace(Duration.ofHours(1), Duration.ZERO)

    table.toStream()
        .peek { _, value ->
            log.info { "[aggregateSearchLog] SearchLogDto: $value" }
            searchLogRepository.save(
            	... 중략
            )
        }
        .map { _, value -> KeyValue(value.query, value) }
        .groupByKey(Grouped.with(Serdes.String(), searchLogDtoSerde()))
        .windowedBy(timeWindow)
        .count(Materialized.with(Serdes.String(), Serdes.Long()))
        .toStream()
        .foreach { windowedKey, count ->
        		... 중략

            searchLogAggregateRepository.upsert(
                Timestamp.from(windowStart),
                Timestamp.from(windowEnd),
                keyword,
                count
            )

            val wasSet = redisTemplate.opsForValue().setIfAbsent(
                "trending:keywords:surge:done:$nowHourKey", "1", Duration.ofHours(24)
            )
            if (wasSet == true) {
                surgeKeywordAnalyzer.updateSurgingKeywordsRedis("prod", nowHourKey)
            }
        }
}
```

이 함수 안에 너무 많은 일이 담겨 있었기에, `+eval: __this.code.searchlog` 명령을 통해 구조 평가를 수행했습니다.

---

### 🧭 리팩토링 설계 흐름 (DSL 기반)

이후 DSL 기반 명령어를 활용해 단계적으로 구조 개선을 진행했습니다:

1. `+action: aggregateSearchLog() → step1: persistDB, step2: updateRedis, step3: triggerSurgeAnalysis`
    → 책임 분리와 단일 목적 함수 분할
2. `+보강: 검색량이 적을때도 문제없도록 방어로직 추가`
    → count <= 0, blank keyword 방지
3. `+보강: 주석추가, dev 분기 제거`
    → 환경 단일화, 코드 단순화
4. `+글쓰기: 자기 주도적 선택과 GPT 협업 기록 블로그화`
    → 리팩토링 흐름을 글로 구조화
5. `+critic` 및 `+탈고`
    → 문서의 흐름, 마무리, 표현력 보강

---

### ✅ 최종 구조 예시 (리팩토링 이후)

```kotlin
private fun persistSearchLog(value: SearchLogDto) { ... }
private fun updateRedis(keyword: String, windowEnd: Long, count: Long) { ... }
private fun triggerSurgeAnalysis(keyword: String, windowStart: Long, windowEnd: Long, count: Long) { ... }
```

위와 같이 구조가 분리된 후, 단위 테스트와 문제 위치 추적이 훨씬 쉬워졌습니다. 핵심 흐름은 유지하면서도, 각 처리 단계를 명확하게 분리하여 유지보수성이 향상되었습니다.

---

### 📍 마무리: 구조화된 실험과 자기주도적 개선

DSL 기반 리팩토링 실험을 통해 얻은 것은 **자신의 맥락과 구조를 재귀적으로 조율해가며 문제를 해결할 수 있는 시스템화된 사고 방식**

GPT를 통해 얻은 개선은 단지 코드 품질이 아니라, **설계 과정 그 자체의 추론 가능성**입니다.