import logging
import os
import time
import psutil

from django.conf import settings
from django.db import connections
from django.utils.deprecation import MiddlewareMixin


def info(smg):
    print(smg)


class VerboseInfoMiddleware(MiddlewareMixin):

    def process_request(self, request):
        mem_before = psutil.Process(os.getpid()).memory_info()
        now = time.time()
        response = self.get_response(request)
        mem_after = psutil.Process(os.getpid()).memory_info()

        if settings.DEBUG:
            queries_count = 0
            queries = []
            for conn in connections.all():
                queries_count += len(conn.queries)
                queries.extend(conn.queries)
            sql_exec_time = round(sum([
                float(q["time"]) for q in queries
            ]), 6)
            try:
                max_sql_exec_time = max([
                    float(q["time"]) for q in queries
                ])
            except ValueError:
                max_sql_exec_time = 0
            info("==== Verbose info ====")
            if getattr(request, 'user', None) is not None:
                info(f"| Authorized: {request.user}")
            else:
                info(f"| Unauthorized")
            if getattr(request, "store", None) is not None:
                info(f"| Store: {request.store.name}")
            info(f"| Endpoint: {request.path}")
            info(f"| Method: {request.method.upper()}")
            info(f"| Execution time: {round(time.time() - now, 6)}s")
            info(f"| Queries count: {queries_count}")
            info(f"| SQL execution time: {sql_exec_time}s")
            info(f"| Slowest SQL execution time: {max_sql_exec_time}s")
            if queries_count > 0:
                info(
                    f"| Average SQL execution time:"
                    f" {round(sql_exec_time / queries_count, 6)}s"
                )
            info(
                f"| Memory used:"
                f" {round((mem_after.rss - mem_before.rss) / 1024):,} Kb"
            )
            info(f"| Queries:")
            for conn in connections.all():
                for idx, q in enumerate(conn.queries):
                    info(f"| {idx + 1}: {q}")
            info("======================")
        return response
