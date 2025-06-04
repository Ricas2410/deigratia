"""
Performance monitoring command for high concurrency environments.
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import connections
from django.conf import settings
import redis
import time
import psutil
import json


class Command(BaseCommand):
    help = 'Monitor system performance for high concurrency'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=10,
            help='Monitoring interval in seconds (default: 10)',
        )
        parser.add_argument(
            '--duration',
            type=int,
            default=300,
            help='Total monitoring duration in seconds (default: 300)',
        )

    def handle(self, *args, **options):
        interval = options['interval']
        duration = options['duration']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting performance monitoring for {duration}s...')
        )
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            stats = self.collect_stats()
            self.display_stats(stats)
            time.sleep(interval)
        
        self.stdout.write(
            self.style.SUCCESS('Performance monitoring completed!')
        )

    def collect_stats(self):
        """Collect system and application statistics."""
        stats = {
            'timestamp': time.time(),
            'system': self.get_system_stats(),
            'database': self.get_database_stats(),
            'cache': self.get_cache_stats(),
            'redis': self.get_redis_stats(),
        }
        return stats

    def get_system_stats(self):
        """Get system resource statistics."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used_gb': psutil.virtual_memory().used / (1024**3),
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
        }

    def get_database_stats(self):
        """Get database connection statistics."""
        db_stats = {}
        
        for alias in connections:
            connection = connections[alias]
            try:
                with connection.cursor() as cursor:
                    # MySQL specific queries
                    if 'mysql' in connection.settings_dict['ENGINE']:
                        cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
                        result = cursor.fetchone()
                        db_stats[alias] = {
                            'connected_threads': int(result[1]) if result else 0,
                            'engine': 'mysql'
                        }
                        
                        cursor.execute("SHOW STATUS LIKE 'Queries'")
                        result = cursor.fetchone()
                        db_stats[alias]['total_queries'] = int(result[1]) if result else 0
                    else:
                        db_stats[alias] = {
                            'engine': connection.settings_dict['ENGINE'],
                            'status': 'connected'
                        }
            except Exception as e:
                db_stats[alias] = {'error': str(e)}
        
        return db_stats

    def get_cache_stats(self):
        """Get Django cache statistics."""
        cache_stats = {}
        
        try:
            # Test cache performance
            start_time = time.time()
            cache.set('perf_test', 'test_value', 60)
            cache.get('perf_test')
            cache.delete('perf_test')
            response_time = (time.time() - start_time) * 1000  # ms
            
            cache_stats['response_time_ms'] = response_time
            cache_stats['status'] = 'working'
        except Exception as e:
            cache_stats['error'] = str(e)
        
        return cache_stats

    def get_redis_stats(self):
        """Get Redis statistics."""
        redis_stats = {}
        
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            info = r.info()
            
            redis_stats = {
                'connected_clients': info.get('connected_clients', 0),
                'used_memory_mb': info.get('used_memory', 0) / (1024**2),
                'used_memory_peak_mb': info.get('used_memory_peak', 0) / (1024**2),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'instantaneous_ops_per_sec': info.get('instantaneous_ops_per_sec', 0),
            }
            
            # Calculate hit ratio
            hits = redis_stats['keyspace_hits']
            misses = redis_stats['keyspace_misses']
            if hits + misses > 0:
                redis_stats['hit_ratio'] = hits / (hits + misses) * 100
            else:
                redis_stats['hit_ratio'] = 0
                
        except Exception as e:
            redis_stats['error'] = str(e)
        
        return redis_stats

    def display_stats(self, stats):
        """Display statistics in a readable format."""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats['timestamp']))
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Performance Stats - {timestamp}")
        self.stdout.write(f"{'='*60}")
        
        # System stats
        sys_stats = stats['system']
        self.stdout.write(f"🖥️  SYSTEM:")
        self.stdout.write(f"   CPU: {sys_stats['cpu_percent']:.1f}%")
        self.stdout.write(f"   Memory: {sys_stats['memory_percent']:.1f}% ({sys_stats['memory_used_gb']:.1f}GB)")
        self.stdout.write(f"   Disk: {sys_stats['disk_usage_percent']:.1f}%")
        self.stdout.write(f"   Network Connections: {sys_stats['network_connections']}")
        
        # Database stats
        db_stats = stats['database']
        self.stdout.write(f"\n💾 DATABASE:")
        for alias, db_info in db_stats.items():
            if 'error' in db_info:
                self.stdout.write(f"   {alias}: ❌ {db_info['error']}")
            else:
                self.stdout.write(f"   {alias}: ✅ {db_info.get('engine', 'unknown')}")
                if 'connected_threads' in db_info:
                    self.stdout.write(f"      Connections: {db_info['connected_threads']}")
                if 'total_queries' in db_info:
                    self.stdout.write(f"      Total Queries: {db_info['total_queries']}")
        
        # Cache stats
        cache_stats = stats['cache']
        self.stdout.write(f"\n🚀 CACHE:")
        if 'error' in cache_stats:
            self.stdout.write(f"   Django Cache: ❌ {cache_stats['error']}")
        else:
            self.stdout.write(f"   Django Cache: ✅ {cache_stats['response_time_ms']:.2f}ms")
        
        # Redis stats
        redis_stats = stats['redis']
        self.stdout.write(f"\n🔴 REDIS:")
        if 'error' in redis_stats:
            self.stdout.write(f"   Redis: ❌ {redis_stats['error']}")
        else:
            self.stdout.write(f"   Clients: {redis_stats['connected_clients']}")
            self.stdout.write(f"   Memory: {redis_stats['used_memory_mb']:.1f}MB (Peak: {redis_stats['used_memory_peak_mb']:.1f}MB)")
            self.stdout.write(f"   Hit Ratio: {redis_stats['hit_ratio']:.1f}%")
            self.stdout.write(f"   Ops/sec: {redis_stats['instantaneous_ops_per_sec']}")
        
        # Performance warnings
        self.check_performance_warnings(stats)

    def check_performance_warnings(self, stats):
        """Check for performance issues and display warnings."""
        warnings = []
        
        # System warnings
        if stats['system']['cpu_percent'] > 80:
            warnings.append("⚠️  High CPU usage!")
        if stats['system']['memory_percent'] > 85:
            warnings.append("⚠️  High memory usage!")
        
        # Redis warnings
        redis_stats = stats['redis']
        if 'hit_ratio' in redis_stats and redis_stats['hit_ratio'] < 80:
            warnings.append("⚠️  Low Redis hit ratio!")
        
        # Cache warnings
        cache_stats = stats['cache']
        if 'response_time_ms' in cache_stats and cache_stats['response_time_ms'] > 100:
            warnings.append("⚠️  Slow cache response time!")
        
        if warnings:
            self.stdout.write(f"\n⚠️  WARNINGS:")
            for warning in warnings:
                self.stdout.write(f"   {warning}")
        else:
            self.stdout.write(f"\n✅ All systems performing well!")
