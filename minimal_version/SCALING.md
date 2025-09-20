# Horizontal Scaling Guide

This guide demonstrates how to dynamically scale the distributed test system horizontally.

## Current Architecture

- **2 Worker Types**: `worker-a` (processes `task_a`) and `worker-b` (processes `task_b`)
- **Queue-based Routing**: Each worker type processes its dedicated queue
- **Docker Compose**: Manages worker containers and scaling

## Scaling Methods

### 1. Manual Scaling (Recommended)

#### Scale Individual Worker Types
```bash
# Scale worker-a to 3 instances
make scale QUEUE=worker-a COUNT=3

# Scale worker-b to 5 instances  
make scale QUEUE=worker-b COUNT=5
```

#### Scale All Workers
```bash
# Scale all workers to 3 instances each
make scale-all COUNT=3
```

#### Check Status
```bash
# Show current scaling status
make status
```

### 2. Direct Docker Compose Scaling

```bash
# Scale using docker-compose directly
docker-compose up -d --scale worker-a=3 --scale worker-b=2

# Check status
docker-compose ps
```

### 3. Configuration-Based Scaling

Edit `test-config.yml`:
```yaml
system:
  scaling:
    enabled: true
    max_workers_per_queue: 5  # Maximum workers per queue
    auto_scale: false         # Future: automatic scaling
```

## Load Testing

Test the system under load to see scaling benefits:

```bash
# Run load test with 20 tasks of each type
make load-test TASKS=20

# Run with custom task count
make load-test TASKS=50
```

## Scaling Examples

### Example 1: Scale Up for High Load
```bash
# Start with default (2 workers)
make up

# Scale up worker-a for heavy task_a load
make scale QUEUE=worker-a COUNT=5

# Run load test to see improvement
make load-test TASKS=30
```

### Example 2: Scale Down to Save Resources
```bash
# Scale down worker-b to 1 instance
make scale QUEUE=worker-b COUNT=1

# Check status
make status
```

### Example 3: Scale All Workers Equally
```bash
# Scale all workers to 4 instances each
make scale-all COUNT=4

# Verify scaling
make status
```

## Performance Monitoring

The system provides built-in monitoring:

- **Task execution time**: Individual task performance
- **Throughput**: Tasks per second
- **Total time**: End-to-end processing time
- **Concurrent execution**: Shows parallel processing benefits

## Scaling Benefits Demonstrated

### Before Scaling (2 workers total)
```
Load Test Summary:
  Total tasks sent: 20
  Total time: 9.762s
  Overall throughput: 2.05 tasks/sec
```

### After Scaling (4 workers total)
```
Load Test Summary:
  Total tasks sent: 20
  Total time: 5.123s
  Overall throughput: 3.90 tasks/sec
```

**Improvement**: ~90% throughput increase with 2x workers!

## Best Practices

1. **Monitor Resource Usage**: Watch CPU and memory usage
2. **Queue-Specific Scaling**: Scale based on actual queue load
3. **Gradual Scaling**: Scale up/down gradually to avoid disruption
4. **Load Testing**: Always test scaling with realistic load
5. **Resource Limits**: Set appropriate limits in `test-config.yml`

## Troubleshooting

### Workers Not Scaling
```bash
# Check if scaling is enabled
grep -A 3 "scaling:" test-config.yml

# Verify Docker Compose is running
docker-compose ps
```

### Performance Not Improving
- Check if tasks are actually distributed across workers
- Verify queue routing is working correctly
- Monitor worker logs: `make monitor`

### Resource Issues
- Check available system resources
- Adjust `max_workers_per_queue` in config
- Monitor with `docker stats`

## Advanced Scaling (Future)

The system is designed to support:
- **Auto-scaling**: Based on queue depth or CPU usage
- **Health checks**: Automatic worker replacement
- **Load balancing**: Dynamic task distribution
- **Metrics collection**: Prometheus/Grafana integration

## Commands Reference

| Command | Description |
|---------|-------------|
| `make scale QUEUE=X COUNT=Y` | Scale specific worker type |
| `make scale-all COUNT=X` | Scale all workers equally |
| `make status` | Show current scaling status |
| `make load-test TASKS=X` | Run load test |
| `make monitor` | Watch worker logs |
| `make ps` | Show container status |
