import asyncio
import json
import os

from fastmcp import Client

SERVER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")


async def run_tests(client: Client) -> None:
    print("=" * 60)
    print(" Cliente APOD MCP - Casos de prueba")
    print("=" * 60)

    await client.ping()
    print("\n[OK] Ping al servidor exitoso\n")

    tools = await client.list_tools()
    print(f"Herramientas disponibles: {[t.name for t in tools]}\n")

    resources = await client.list_resources()
    print(f"Recursos disponibles: {[str(r.uri) for r in resources]}\n")

    templates = await client.list_resource_templates()
    print(f"Templates de recursos: {[t.uriTemplate for t in templates]}\n")

    print("=" * 60)
    print(" TESTS: Tools")
    print("=" * 60)

    tool_test_cases = [
        {
            "label": "CP-01: APOD del dia (sin parametros)",
            "args": {},
            "expect_error": False,
        },
        {
            "label": "CP-02: APOD de fecha especifica (2024-01-01)",
            "args": {"date": "2024-01-01"},
            "expect_error": False,
        },
        {
            "label": "CP-03: Fecha invalida formato (01-01-2024)",
            "args": {"date": "01-01-2024"},
            "expect_error": True,
        },
        {
            "label": "CP-04: APOD con HD=true",
            "args": {"hd": True},
            "expect_error": False,
        },
        {
            "label": "CP-05: Fecha anterior al inicio de APOD (1995-06-15)",
            "args": {"date": "1995-06-15"},
            "expect_error": True,
        },
        {
            "label": "CP-06: Fecha futura (2050-01-01)",
            "args": {"date": "2050-01-01"},
            "expect_error": True,
        },
    ]

    passed = 0
    failed = 0

    for tc in tool_test_cases:
        print("-" * 60)
        print(f"  {tc['label']}")
        print(f"  Argumentos: {json.dumps(tc['args'])}")
        print()
        try:
            result = await client.call_tool("get_apod_info", tc["args"])
            if tc["expect_error"]:
                print(f"  FALLO: Se esperaba error pero se obtuvo resultado")
                failed += 1
            else:
                print(f"  OK - Resultado:")
                for item in result.data if not isinstance(result.data, dict) else [result.data]:
                    print(f"    {json.dumps(item, indent=2, ensure_ascii=False)[:500]}...")
                passed += 1
        except Exception as exc:
            if tc["expect_error"]:
                print(f"  OK - Error esperado: {exc}")
                passed += 1
            else:
                print(f"  FALLO - Error inesperado: {exc}")
                failed += 1
        print()

    print("=" * 60)
    print(f"  Resultados Tools: {passed} pasados, {failed} fallidos de {len(tool_test_cases)}")
    print("=" * 60)

    print()
    print("=" * 60)
    print(" TESTS: Resources JSON")
    print("=" * 60)

    json_resource_tests = [
        {"label": "CR-01: JSON resource fecha valida", "uri": "apod://json/2024-01-01", "expect_error": False},
        {"label": "CR-02: JSON resource con query param hd", "uri": "apod://json/2024-01-01?hd=true", "expect_error": False},
        {"label": "CR-03: JSON resource fecha invalida", "uri": "apod://json/01-01-2024", "expect_error": True},
        {"label": "CR-04: JSON resource fecha futura", "uri": "apod://json/2050-01-01", "expect_error": True},
    ]

    for rc in json_resource_tests:
        print("-" * 60)
        print(f"  {rc['label']}")
        print(f"  URI: {rc['uri']}")
        print()
        try:
            result = await client.read_resource(rc["uri"])
            if rc["expect_error"]:
                print(f"  FALLO: Se esperaba error pero se obtuvo resultado")
                failed += 1
            else:
                print(f"  OK - MIME type: {result.content.mimeType if hasattr(result, 'content') else 'N/A'}")
                data = json.loads(result.content.text) if hasattr(result, 'content') and hasattr(result.content, 'text') else result.data
                if isinstance(data, dict):
                    print(f"       Title: {data.get('title', 'N/A')}")
                    print(f"       Date: {data.get('date', 'N/A')}")
                passed += 1
        except Exception as exc:
            if rc["expect_error"]:
                print(f"  OK - Error esperado: {exc}")
                passed += 1
            else:
                print(f"  FALLO - Error inesperado: {exc}")
                failed += 1
        print()

    print("=" * 60)
    print(" TESTS: Resources Markdown")
    print("=" * 60)

    md_resource_tests = [
        {"label": "CR-05: Markdown resource fecha valida", "uri": "apod://markdown/2024-01-01", "expect_error": False},
        {"label": "CR-06: Markdown resource con query param hd", "uri": "apod://markdown/2024-01-01?hd=true", "expect_error": False},
    ]

    for rc in md_resource_tests:
        print("-" * 60)
        print(f"  {rc['label']}")
        print(f"  URI: {rc['uri']}")
        print()
        try:
            result = await client.read_resource(rc["uri"])
            if rc["expect_error"]:
                print(f"  FALLO: Se esperaba error pero se obtuvo resultado")
                failed += 1
            else:
                print(f"  OK - MIME type: {result.content.mimeType if hasattr(result, 'content') else 'N/A'}")
                content = result.content.text if hasattr(result, 'content') and hasattr(result.content, 'text') else str(result.data)
                print(f"       Preview (primeras 300 chars):")
                print(f"       {content[:300]}...")
                passed += 1
        except Exception as exc:
            if rc["expect_error"]:
                print(f"  OK - Error esperado: {exc}")
                passed += 1
            else:
                print(f"  FALLO - Error inesperado: {exc}")
                failed += 1
        print()

    print("=" * 60)
    print(" TESTS: Resources Image")
    print("=" * 60)

    img_resource_tests = [
        {"label": "CR-07: Image resource fecha valida", "uri": "apod://image/2024-01-01", "expect_error": False},
    ]

    for rc in img_resource_tests:
        print("-" * 60)
        print(f"  {rc['label']}")
        print(f"  URI: {rc['uri']}")
        print()
        try:
            result = await client.read_resource(rc["uri"])
            if rc["expect_error"]:
                print(f"  FALLO: Se esperaba error pero se obtuvo resultado")
                failed += 1
            else:
                print(f"  OK - MIME type: {result.content.mimeType if hasattr(result, 'content') else 'N/A'}")
                blob = result.content.blob if hasattr(result, 'content') and hasattr(result.content, 'blob') else result.data
                if isinstance(blob, str):
                    import base64
                    blob = base64.b64decode(blob)
                print(f"       Image size: {len(blob)} bytes")
                passed += 1
        except Exception as exc:
            if rc["expect_error"]:
                print(f"  OK - Error esperado: {exc}")
                passed += 1
            else:
                print(f"  FALLO - Error inesperado: {exc}")
                failed += 1
        print()

    print("=" * 60)
    print(f"  Resultados Resources: {passed - 6} pasados adicionales")
    print("=" * 60)

    print()
    print("-" * 60)
    print("  CP-07: Rate limit - tools solo (esperar ventana)")
    print()
    print("  Esperando 61s para que se reinicie la ventana de rate limit...")
    await asyncio.sleep(61)

    blocked_at = None
    for i in range(1, 7):
        try:
            await client.call_tool("get_apod_info", {})
            print(f"  Tool peticion {i}: OK")
        except Exception as exc:
            err = str(exc)
            if "Rate limit excedido" in err:
                print(f"  Tool peticion {i}: BLOQUEADA (rate limit) - {exc}")
                blocked_at = i
                break
            else:
                print(f"  Tool peticion {i}: ERROR NASA (no es rate limit) - {exc}")
        await asyncio.sleep(0.2)

    print()
    if blocked_at is not None:
        print(f"  OK - Rate limit funciono en tool peticion {blocked_at}")
    else:
        print(f"  FALLO - Rate limit no se activo tras 6 tool peticiones")
    print("-" * 60)

    print()
    print("-" * 60)
    print("  CP-08: Rate limit NO aplica a resources")
    print()
    print("  Haciendo 10 peticiones de resource sin esperar...")
    
    resource_blocked = False
    for i in range(1, 11):
        try:
            await client.read_resource("apod://json/2024-01-01")
            print(f"  Resource peticion {i}: OK")
        except Exception as exc:
            err = str(exc)
            if "Rate limit" in err:
                print(f"  Resource peticion {i}: BLOQUEADA - {exc}")
                resource_blocked = True
                break
            else:
                print(f"  Resource peticion {i}: ERROR (no rate limit) - {exc}")
        await asyncio.sleep(0.1)

    print()
    if not resource_blocked:
        print(f"  OK - Resources NO tienen rate limit (10 peticiones sin bloqueo)")
    else:
        print(f"  FALLO - Resources fueron bloqueados por rate limit")
    print("-" * 60)

    print()
    print("-" * 60)
    print("  CP-09: Cache - verificar que la segunda peticion es cacheada")
    print()
    
    import time as time_module
    
    test_date = "2024-01-01"
    
    print(f"  Realizando primera peticion (cache MISS)...")
    start = time_module.time()
    try:
        result1 = await client.read_resource(f"apod://json/{test_date}")
        first_duration = time_module.time() - start
        print(f"  Primera peticion: {first_duration:.3f}s - OK")
    except Exception as exc:
        print(f"  Primera peticion: ERROR - {exc}")
        first_duration = None
    
    print()
    print(f"  Realizando segunda peticion (cache HIT)...")
    start = time_module.time()
    try:
        result2 = await client.read_resource(f"apod://json/{test_date}")
        second_duration = time_module.time() - start
        print(f"  Segunda peticion: {second_duration:.3f}s - OK")
    except Exception as exc:
        print(f"  Segunda peticion: ERROR - {exc}")
        second_duration = None
    
    print()
    if first_duration and second_duration:
        if second_duration < first_duration:
            speedup = first_duration / second_duration
            print(f"  OK - Cache funcionando: {second_duration:.3f}s < {first_duration:.3f}s ({speedup:.1f}x mas rapido)")
        else:
            print(f"  WARNING - Segunda peticion no fue mas rapida (posible cache MISS)")
    print("-" * 60)

    print()
    print("-" * 60)
    print("  CP-10: Cache - imagen segunda peticion debe ser cacheada")
    print()
    
    print(f"  Realizando primera peticion de imagen (cache MISS)...")
    start = time_module.time()
    try:
        result1 = await client.read_resource(f"apod://image/{test_date}")
        first_duration = time_module.time() - start
        print(f"  Primera peticion: {first_duration:.3f}s - OK")
    except Exception as exc:
        print(f"  Primera peticion: ERROR - {exc}")
        first_duration = None
    
    print()
    print(f"  Realizando segunda peticion de imagen (cache HIT)...")
    start = time_module.time()
    try:
        result2 = await client.read_resource(f"apod://image/{test_date}")
        second_duration = time_module.time() - start
        print(f"  Segunda peticion: {second_duration:.3f}s - OK")
    except Exception as exc:
        print(f"  Segunda peticion: ERROR - {exc}")
        second_duration = None
    
    print()
    if first_duration and second_duration:
        if second_duration < first_duration:
            speedup = first_duration / second_duration
            print(f"  OK - Cache imagen funcionando: {second_duration:.3f}s < {first_duration:.3f}s ({speedup:.1f}x mas rapido)")
        else:
            print(f"  WARNING - Segunda peticion no fue mas rapida")
    print("-" * 60)


async def main() -> None:
    client = Client(SERVER_FILE)

    async with client:
        await run_tests(client)


if __name__ == "__main__":
    asyncio.run(main())